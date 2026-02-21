import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException

from config.settings import Config
from helpers.data_generator import DataGenerator, APIHelper


def pytest_addoption(parser):
    """Добавление опций командной строки."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Выберите браузер: chrome или firefox",
        choices=["chrome", "firefox"]
    )


@pytest.fixture(scope="function")
def browser_name(request):
    """Фикстура для получения имени браузера из командной строки."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="function")
def driver(browser_name):
    """
    Фикстура для инициализации WebDriver.
    
    Поддерживает Chrome и Firefox.
    Параметр --browser позволяет выбрать браузер из командной строки.
    
    Примеры использования:
        pytest --browser=chrome
        pytest --browser=firefox
    """
    driver_instance = None
    
    with allure.step(f"Запуск браузера: {browser_name}"):
        try:
            if browser_name == "chrome":
                options = webdriver.ChromeOptions()
                options.add_argument("--start-maximized")
                options.add_argument("--disable-blink-features=AutomationControlled")
                
                driver_instance = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
                
            elif browser_name == "firefox":
                options = webdriver.FirefoxOptions()
                
                driver_instance = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )
                driver_instance.maximize_window()
            
            # Устанавливаем неявное ожидание
            driver_instance.implicitly_wait(Config.IMPLICIT_WAIT)
            
        except WebDriverException as e:
            pytest.fail(f"Не удалось запустить браузер {browser_name}. Ошибка: {e}")
    
    yield driver_instance
    
    with allure.step(f"Закрытие браузера: {browser_name}"):
        if driver_instance:
            driver_instance.quit()


@pytest.fixture(scope="function")
def random_user():
    """
    Фикстура для создания случайного пользователя через API.
    
    Создает пользователя перед тестом и удаляет после.
    
    Yields:
        tuple: (email, password) созданного пользователя
    """
    # Генерация данных
    payload = DataGenerator.generate_user_payload()
    email = payload["email"]
    password = payload["password"]
    
    # Создание пользователя
    with allure.step(f"Setup: Создание пользователя {email}"):
        access_token, _ = APIHelper.create_user(payload, Config)
    
    # Передача данных в тест
    yield email, password
    
    # Удаление пользователя
    with allure.step(f"Teardown: Удаление пользователя {email}"):
        APIHelper.delete_user(access_token, Config)


@pytest.fixture(scope="function")
def authorized_user(driver, random_user):
    """
    Фикстура для авторизованного пользователя.
    
    Создает пользователя, выполняет вход и передает в тест.
    
    Yields:
        tuple: (driver, email, password)
    """
    email, password = random_user
    
    # Авторизация
    with allure.step(f"Setup: Авторизация пользователя {email}"):
        from pages.login_page import LoginPage
        
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(email, password)
    
    yield driver, email, password


# Hooks для Allure отчетов
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook для добавления скриншотов в Allure при падении тестов.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Получаем driver из фикстуры
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            
            # Делаем скриншот
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG
            )
            
            # Добавляем HTML страницы
            allure.attach(
                driver.page_source,
                name="Page HTML on failure",
                attachment_type=allure.attachment_type.HTML
            )
            