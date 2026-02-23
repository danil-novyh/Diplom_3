import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException
)
from typing import Tuple


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator):
        """Поиск элемента с ожиданием."""
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Элемент {locator} не найден"
        )
    
    @allure.step("Ожидание видимости элемента: {locator}")
    def wait_for_visible(self, locator):
        """Ожидание видимости элемента."""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    @allure.step("Ожидание кликабельности элемента: {locator}")
    def wait_for_clickable(self, locator):
        """Ожидание возможности клика."""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    @allure.step("Клик по элементу через JavaScript: {locator}")
    def click_via_js(self, locator):
        """Клик через JavaScript (для сложных случаев)."""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true); arguments[0].click();",
            element
        )
    
    @allure.step("Умный клик по элементу: {locator}")
    def smart_click(self, locator):
        """
        Клик с обработкой StaleElementReferenceException
        и ElementClickInterceptedException.
        """
        try:
            element = self.wait_for_clickable(locator)
            element.click()
        except (StaleElementReferenceException, ElementClickInterceptedException):
            # Повторная попытка через JS
            self.click_via_js(locator)
    
    @allure.step("Drag and Drop через JavaScript")
    def drag_and_drop_js(self, source_locator, target_locator):
        """
        Drag and Drop через JavaScript.
        Работает в Chrome и Firefox.
        """
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        
        # JavaScript для эмуляции drag-and-drop
        js_code = """
        function createEvent(typeOfEvent) {
            var event = document.createEvent("CustomEvent");
            event.initCustomEvent(typeOfEvent, true, true, null);
            event.dataTransfer = {
                data: {},
                setData: function (key, value) { this.data[key] = value; },
                getData: function (key) { return this.data[key]; }
            };
            return event;
        }
        
        function dispatchEvent(element, event, transferData) {
            if (transferData !== undefined) {
                event.dataTransfer = transferData;
            }
            if (element.dispatchEvent) {
                element.dispatchEvent(event);
            } else if (element.fireEvent) {
                element.fireEvent("on" + event.type, event);
            }
        }
        
        var source = arguments[0];
        var target = arguments[1];
        
        var dragStartEvent = createEvent('dragstart');
        dispatchEvent(source, dragStartEvent);
        
        var dropEvent = createEvent('drop');
        dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);
        
        var dragEndEvent = createEvent('dragend');
        dispatchEvent(source, dragEndEvent, dropEvent.dataTransfer);
        """
        
        self.driver.execute_script(js_code, source, target)
    
    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator):
        """Получение текста элемента."""
        return self.find_element(locator).text
    
    @allure.step("Ввести текст в поле: {locator}")
    def send_keys(self, locator, text):
        """Ввод текста."""
        element = self.wait_for_clickable(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.driver.current_url
    
    @allure.step("Ожидание исчезновения элемента: {locator}")
    def wait_for_invisibility(self, locator):
        """Ожидание исчезновения элемента."""
        self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Открыть URL: {url}")
    def open_url(self, url: str):
        """Открытие страницы по URL."""
        self.driver.get(url)

    @allure.step("Обновить страницу")
    def refresh(self):
        """Обновление текущей страницы."""
        self.driver.refresh()

    @allure.step("Проверить наличие элемента: {locator}")
    def is_element_present(self, locator) -> bool:
        """Проверка наличия элемента на странице."""
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False