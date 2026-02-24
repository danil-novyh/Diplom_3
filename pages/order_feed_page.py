import allure
from pages.base_page import BasePage
from locators.order_feed_page_locators import OrderFeedPageLocators
from config.settings import Config


class OrderFeedPage(BasePage):
    """Класс для взаимодействия с лентой заказов."""
    
    @allure.step("Открыть страницу 'Лента заказов'")
    def open(self):
        """Открытие страницы ленты заказов."""
        self.open_url(Config.FEED_URL)
        self.wait_for_page_load()
    
    @allure.step("Ожидание загрузки страницы ленты заказов")
    def wait_for_page_load(self):
        """Ожидание загрузки ключевых элементов."""
        self.wait_for_visible(OrderFeedPageLocators.PAGE_TITLE)
        self.wait_for_visible(OrderFeedPageLocators.ALL_TIME_COUNTER)
    
    @allure.step("Обновить страницу и дождаться загрузки")
    def refresh_page(self):
        """Обновление страницы для получения актуальных данных."""
        self.refresh()
        self.wait_for_page_load()
    
    @allure.step("Получить значение счетчика 'Выполнено за все время'")
    def get_all_time_counter(self) -> int:
        """
        Получение значения счетчика за все время.
        
        Returns:
            int: Количество заказов за все время
        """
        counter_text = self.get_text(OrderFeedPageLocators.ALL_TIME_COUNTER)
        # Убираем пробелы и запятые
        clean_text = counter_text.replace(" ", "").replace(",", "")
        return int(clean_text)
    
    @allure.step("Получить значение счетчика 'Выполнено за сегодня'")
    def get_today_counter(self) -> int:
        """
        Получение значения счетчика за сегодня.
        
        Returns:
            int: Количество заказов за сегодня
        """
        counter_text = self.get_text(OrderFeedPageLocators.TODAY_COUNTER)
        # Убираем пробелы и запятые
        clean_text = counter_text.replace(" ", "").replace(",", "")
        return int(clean_text)
    
    @allure.step("Проверить наличие заказа #{order_number} в разделе 'В работе'")
    def is_order_in_progress(self, order_number) -> bool:
        """
        Проверка наличия заказа в разделе 'В работе'.
        Сравнивает номера заказов как строки, игнорируя ведущие нули.
        
        Аргументы:
            order_number: Номер заказа (строка или число)
        
        Возвращает:
            bool: True если заказ найден в разделе 'В работе'
        """
        # Преобразуем номер заказа в строку и удаляем ведущие нули
        target_str = str(order_number).lstrip('0') or '0'
        
        # Получаем все элементы заказов в разделе "В работе"
        order_elements = self.find_elements(OrderFeedPageLocators.IN_PROGRESS_ORDERS)
        
        # Проверяем каждый заказ
        for order_element in order_elements:
            order_text = order_element.text.strip()
            
            # Убираем символ '#' и пробелы
            order_clean = order_text.replace('#', '').replace(' ', '').strip()
            
            # Удаляем ведущие нули из номера заказа на странице
            order_number_clean = order_clean.lstrip('0') or '0'
            
            # Сравниваем очищенные строки (без ведущих нулей)
            if order_number_clean == target_str:
                return True
        
        return False
    
    @allure.step("Получить список всех заказов 'В работе'")
    def get_orders_in_progress(self) -> list:
        """
        Получение списка всех номеров заказов в работе.
        
        Returns:
            list: Список номеров заказов
        """
        orders = self.find_elements(OrderFeedPageLocators.IN_PROGRESS_ORDERS)
        return [order.text.strip().replace("#", "") for order in orders]
    