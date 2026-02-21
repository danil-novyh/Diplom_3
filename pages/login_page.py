import allure
from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from config.settings import Config


class LoginPage(BasePage):
    """Класс для взаимодействия со страницей входа."""
    
    @allure.step("Открыть страницу авторизации")
    def open(self):
        """Открытие страницы логина."""
        self.driver.get(Config.LOGIN_URL)
        self.wait_for_page_load()
    
    @allure.step("Ожидание загрузки страницы авторизации")
    def wait_for_page_load(self):
        """Ожидание загрузки ключевых элементов."""
        self.wait_for_visible(LoginPageLocators.LOGIN_TITLE)
        self.wait_for_visible(LoginPageLocators.LOGIN_BUTTON)
    
    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        """
        Ввод email в поле.
        
        Args:
            email: Email пользователя
        """
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
    
    @allure.step("Ввести пароль")
    def enter_password(self, password):
        """
        Ввод пароля в поле.
        
        Args:
            password: Пароль пользователя
        """
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)
    
    @allure.step("Клик по кнопке 'Войти'")
    def click_login_button(self):
        """Клик по кнопке входа."""
        self.smart_click(LoginPageLocators.LOGIN_BUTTON)
    
    @allure.step("Выполнить вход с email: {email}")
    def login(self, email, password):
        """
        Полный процесс авторизации.
        
        Args:
            email: Email пользователя
            password: Пароль пользователя
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        # Ожидание перехода на главную страницу
        from locators.main_page_locators import MainPageLocators
        self.wait_for_visible(MainPageLocators.TITLE_ASSEMBLE_BURGER)
        