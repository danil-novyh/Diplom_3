import allure
import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from config.settings import Config


@allure.epic("UI Tests")
@allure.feature("Основная функциональность")
class TestMainFunctionality:
    """Тесты основного функционала приложения."""
    
    @allure.title("Переход в раздел 'Конструктор' по клику на кнопку")
    @allure.description(
        "Проверка навигации в раздел Конструктор через кнопку в header.\n"
        "Шаги:\n"
        "1. Открыть страницу логина\n"
        "2. Кликнуть 'Конструктор' в header\n"
        "3. Проверить, что произошел переход на главную страницу"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_navigate_to_constructor(self, driver):
        """Проверка перехода в раздел Конструктор."""
        
        # Открываем страницу логина (чтобы быть не на главной)
        login_page = LoginPage(driver)
        login_page.open()
        
        # Кликаем по кнопке Конструктор
        main_page = MainPage(driver)
        main_page.click_constructor_button()
        
        # Проверяем URL и наличие заголовка
        with allure.step("Проверка успешного перехода"):
            current_url = main_page.get_current_url()
            assert current_url == Config.BASE_URL + "/", \
                f"Ожидался URL {Config.BASE_URL}/, получен {current_url}"
            
            assert main_page.is_modal_closed(), \
                "Заголовок 'Соберите бургер' не отображается"
    
    @allure.title("Переход в раздел 'Лента Заказов' по клику на кнопку")
    @allure.description(
        "Проверка навигации в Ленту Заказов через кнопку в header.\n"
        "Шаги:\n"
        "1. Открыть главную страницу\n"
        "2. Кликнуть 'Лента Заказов' в header\n"
        "3. Проверить URL и наличие заголовка"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_navigate_to_order_feed(self, driver):
        """Проверка перехода в Ленту Заказов."""
        
        # Открываем главную страницу
        main_page = MainPage(driver)
        main_page.open()
        
        # Кликаем по кнопке Лента Заказов
        main_page.click_order_feed_button()
        
        # Проверяем переход
        with allure.step("Проверка успешного перехода"):
            current_url = main_page.get_current_url()
            
            assert "/feed" in current_url, \
                f"URL не содержит /feed. Текущий URL: {current_url}"
    
    @allure.title("Открытие модального окна при клике на ингредиент")
    @allure.description(
        "Проверка появления всплывающего окна с деталями ингредиента.\n"
        "Шаги:\n"
        "1. Открыть главную страницу\n"
        "2. Кликнуть на ингредиент\n"
        "3. Проверить открытие модального окна\n"
        "4. Проверить корректность названия ингредиента"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_ingredient_modal_opens(self, driver):
        """Проверка открытия модального окна с деталями ингредиента."""
        
        # Открываем главную страницу
        main_page = MainPage(driver)
        main_page.open()
        
        # Кликаем на ингредиент
        main_page.click_ingredient_fluorescent_bun()
        
        # Проверяем открытие модального окна
        with allure.step("Проверка отображения модального окна и названия ингредиента"):
            assert main_page.is_ingredient_modal_displayed(), \
                "Модальное окно с деталями ингредиента не открылось"
            ingredient_name = main_page.get_ingredient_name_from_modal()
            expected_name = "Флюоресцентная булка R2-D3"
            
            assert ingredient_name == expected_name, \
                f"Ожидалось название '{expected_name}', получено '{ingredient_name}'"
    
    @allure.title("Закрытие модального окна кликом по крестику")
    @allure.description(
        "Проверка закрытия всплывающего окна через кнопку X.\n"
        "Шаги:\n"
        "1. Открыть главную страницу\n"
        "2. Открыть модальное окно ингредиента\n"
        "3. Кликнуть на крестик\n"
        "4. Проверить закрытие окна"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_close_ingredient_modal(self, driver):
        """Проверка закрытия модального окна."""
        
        # Открываем главную страницу
        main_page = MainPage(driver)
        main_page.open()
        
        # Открываем модальное окно
        main_page.click_ingredient_fluorescent_bun()
                
        # Закрываем модальное окно
        main_page.close_modal()
        
        # Проверяем закрытие
        with allure.step("Проверка закрытия модального окна"):
            assert main_page.is_modal_closed(), \
                "Модальное окно не закрылось после клика по крестику"
    
    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    @allure.description(
        "Проверка работы счетчика ингредиентов.\n"
        "Шаги:\n"
        "1. Открыть главную страницу\n"
        "2. Запомнить значение счетчика\n"
        "3. Перетащить ингредиент в конструктор\n"
        "4. Проверить увеличение счетчика"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_ingredient_counter_increases(self, driver):
        """Проверка увеличения счетчика ингредиента."""
        
        # Открываем главную страницу
        main_page = MainPage(driver)
        main_page.open()
        
        # Получаем начальное значение счетчика
        with allure.step("Получение начального значения счетчика"):
            initial_counter = main_page.get_ingredient_counter()
        
        # Добавляем ингредиент в конструктор
        main_page.add_ingredient_to_constructor()
        
        # Получаем новое значение счетчика
        with allure.step("Получение нового значения счетчика"):
            new_counter = main_page.get_ingredient_counter()
        
        # Проверяем увеличение
        with allure.step("Проверка увеличения счетчика"):
            # Булочка добавляется 2 раза (верх + низ)
            expected_counter = initial_counter + 2
            
            assert new_counter == expected_counter, \
                f"Ожидалось {expected_counter}, получено {new_counter}"
            