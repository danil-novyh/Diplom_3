import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.base_page_locators import BasePageLocators
from locators.main_page_locators import MainPageLocators
from config.settings import Config


class MainPage(BasePage):
    """Класс для взаимодействия с главной страницей."""
    
    @allure.step("Открыть главную страницу")
    def open(self):
        """Открытие главной страницы и ожидание загрузки."""
        self.driver.get(Config.BASE_URL)
        self.wait_for_page_load()
    
    @allure.step("Ожидание загрузки главной страницы")
    def wait_for_page_load(self):
        """Ожидание загрузки ключевых элементов страницы."""
        self.wait_for_visible(MainPageLocators.TITLE_ASSEMBLE_BURGER)
        self.wait_for_visible(MainPageLocators.SECTION_BUNS)
    
    @allure.step("Клик по кнопке 'Конструктор' в header")
    def click_constructor_button(self):
        """Переход в раздел Конструктор через header."""
        self.smart_click(BasePageLocators.CONSTRUCTOR_BUTTON)
        self.wait_for_page_load()
    
    @allure.step("Клик по кнопке 'Лента Заказов' в header")
    def click_order_feed_button(self):
        """Переход в ленту заказов через header."""
        self.smart_click(BasePageLocators.ORDER_FEED_BUTTON)
        # Ожидание перехода на другую страницу
        self.wait.until(EC.url_contains("/feed"))
    
    @allure.step("Клик по кнопке 'Личный Кабинет' в header")
    def click_personal_account_button(self):
        """Переход в личный кабинет через header."""
        self.smart_click(BasePageLocators.PERSONAL_ACCOUNT_BUTTON)
    
    @allure.step("Клик по кнопке 'Войти в аккаунт'")
    def click_login_button(self):
        """Клик по главной кнопке входа."""
        self.smart_click(MainPageLocators.LOGIN_BUTTON)
        # Ожидание перехода на страницу логина
        self.wait.until(EC.url_contains("/login"))
    
    @allure.step("Клик по ингредиенту: Флюоресцентная булка R2-D3")
    def click_ingredient_fluorescent_bun(self):
        """Открытие модального окна с деталями ингредиента."""
        self.smart_click(MainPageLocators.INGREDIENT_FLUORESCENT_BUN)
        # Ожидание появления модального окна
        self.wait_for_visible(MainPageLocators.INGREDIENT_DETAILS_TITLE)
    
    @allure.step("Проверка отображения модального окна с деталями ингредиента")
    def is_ingredient_modal_displayed(self):
        """
        Проверка видимости модального окна.
        Возвращает:
            bool: True если окно отображается
        """
        elements = self.driver.find_elements(*MainPageLocators.INGREDIENT_DETAILS_TITLE)
        return len(elements) > 0 and elements[0].is_displayed()
    
    @allure.step("Получить название ингредиента из модального окна")
    def get_ingredient_name_from_modal(self):
        """
        Получение названия ингредиента из модального окна.
        
        Returns:
            str: Название ингредиента
        """
        return self.get_text(MainPageLocators.INGREDIENT_DETAILS_NAME)
    
    @allure.step("Закрыть модальное окно кликом по крестику")
    def close_modal(self):
        """Закрытие модального окна через кнопку X."""
        self.smart_click(BasePageLocators.MODAL_CLOSE_BUTTON)
        # Ожидание исчезновения модального окна
        self.wait_for_invisibility(BasePageLocators.MODAL_OVERLAY)
    
    @allure.step("Проверка, что модальное окно закрыто")
    def is_modal_closed(self):
        """
        Проверка, что модальное окно закрылось.
        Возвращает:
            bool: True если заголовок 'Соберите бургер' виден
        """
        elements = self.driver.find_elements(*MainPageLocators.TITLE_ASSEMBLE_BURGER)
        return len(elements) > 0 and elements[0].is_displayed()
    
    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter(self) -> int:
        """
        Получение значения счетчика ингредиента.
        
        Returns:
            int: Значение счетчика
        """
        if self.is_element_present(MainPageLocators.INGREDIENT_COUNTER):
            counter_text = self.get_text(MainPageLocators.INGREDIENT_COUNTER)
            return int(counter_text)
        return 0
    
    @allure.step("Добавить ингредиент в конструктор через Drag and Drop")
    def add_ingredient_to_constructor(self):
        """Перетаскивание ингредиента в корзину конструктора."""
        self.drag_and_drop_js(
            MainPageLocators.INGREDIENT_FLUORESCENT_BUN,
            MainPageLocators.CONSTRUCTOR_AREA
        )
        # Ожидание появления булочки в конструкторе
        self.wait_for_visible(MainPageLocators.CONSTRUCTOR_BUN_TOP)
    
    @allure.step("Проверка, что ингредиент добавлен в конструктор")
    def is_ingredient_in_constructor(self):
        """
        Проверка наличия ингредиента в конструкторе.
        Возвращает:
            bool: True если ингредиент добавлен
        """
        elements = self.driver.find_elements(*MainPageLocators.CONSTRUCTOR_BUN_TOP)
        return len(elements) > 0 and elements[0].is_displayed()
    
    @allure.step("Клик по кнопке 'Оформить заказ'")
    def click_create_order_button(self):
        """Оформление заказа."""
        self.smart_click(MainPageLocators.CREATE_ORDER_BUTTON)
        # Ожидание появления модального окна с номером заказа
        self.wait_for_order_number()
    
    @allure.step("Ожидание появления номера заказа")
    def wait_for_order_number(self):
        """
        Ожидание появления реального номера заказа.
        Номер должен быть не равен 9999 (заглушка).
        """
        self.wait.until(
            lambda driver: (
                text := self.get_text(MainPageLocators.ORDER_NUMBER_MODAL)
            ) and text.strip().isdigit() and text.strip() != "9999",
            message="Номер заказа не появился или остался 9999"
        )
    
    @allure.step("Получить номер заказа")
    def get_order_number(self):
        """
        Получение номера заказа из модального окна.
        
        Returns:
            str: Номер заказа
        """
        order_text = self.get_text(MainPageLocators.ORDER_NUMBER_MODAL)
        # Убираем пробелы и возвращаем
        return order_text.replace(" ", "").strip()
    
    @allure.step("Закрыть модальное окно с номером заказа")
    def close_order_modal(self):
        """Закрытие модального окна после оформления заказа."""
        self.close_modal()
