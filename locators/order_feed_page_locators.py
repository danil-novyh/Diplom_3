from selenium.webdriver.common.by import By


class OrderFeedPageLocators:
    """Локаторы элементов ленты заказов."""
    
    # Заголовок
    PAGE_TITLE = (
        By.XPATH, 
        "//h1[text()='Лента заказов']"
    )
    
    # Список заказов
    ORDER_LIST = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_list')]"
    )
    
    FIRST_ORDER = (
        By.XPATH,
        "(//li[contains(@class, 'OrderHistory_listItem')])[1]"
    )
    
    # Счетчики
    ALL_TIME_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'text_type_digits-large')]"
    )
    
    TODAY_COUNTER = (
        By.XPATH,
        "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'text_type_digits-large')]"
    )
    
    # Раздел "В работе"
    IN_PROGRESS_SECTION = (
        By.XPATH,
        "//p[text()='В работе:']/following-sibling::ul"
    )
    
    IN_PROGRESS_ORDERS = (
        By.XPATH,
        "//p[text()='В работе:']/following-sibling::ul//li"
    )
    
    # Раздел "Готовы"
    READY_SECTION = (
        By.XPATH,
        "//p[text()='Готовы:']/following-sibling::ul"
    )
    
    @staticmethod
    def get_order_by_number(order_number):
        """
        Динамический локатор для поиска заказа по номеру.
        
        Args:
            order_number: Номер заказа (без ведущих нулей)
        
        Returns:
            tuple: Локатор для конкретного заказа
        """
        # Убираем ведущие нули
        clean_number = str(int(order_number))
        return (
            By.XPATH,
            f"//p[text()='#{clean_number}']"
        )
    