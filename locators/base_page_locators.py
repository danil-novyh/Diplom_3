from selenium.webdriver.common.by import By


class BasePageLocators:
    """Локаторы элементов, общих для всех страниц."""
    
    # Header элементы
    LOGO = (By.XPATH, "//div[@class='AppHeader_header__logo__2D0X2']")
    
    CONSTRUCTOR_BUTTON = (
        By.XPATH, 
        "//p[contains(text(), 'Конструктор')]"
    )
    
    ORDER_FEED_BUTTON = (
        By.XPATH, 
        "//p[contains(text(), 'Лента Заказов')]"
    )
    
    PERSONAL_ACCOUNT_BUTTON = (
        By.XPATH, 
        "//a[@href='/account']"
    )
    
    # Модальные окна
    MODAL_OVERLAY = (
        By.CSS_SELECTOR, 
        "div.Modal_modal__overlay__x2ZCr"
    )
    
    MODAL_CLOSE_BUTTON = (
        By.XPATH, 
        "//button[contains(@class, 'Modal_modal__close')]"
    )
