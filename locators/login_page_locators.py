from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Локаторы элементов страницы входа."""
    
    LOGIN_TITLE = (
        By.XPATH, 
        "//h2[text()='Вход']"
    )
    
    EMAIL_INPUT = (
        By.XPATH, 
        "//label[text()='Email']/following-sibling::input"
    )
    
    PASSWORD_INPUT = (
        By.XPATH, 
        "//input[@name='Пароль']"
    )
    
    LOGIN_BUTTON = (
        By.XPATH, 
        "//button[text()='Войти']"
    )
    
    REGISTER_LINK = (
        By.XPATH, 
        "//a[text()='Зарегистрироваться']"
    )
    
    RESTORE_PASSWORD_LINK = (
        By.XPATH,
        "//a[text()='Восстановить пароль']"
    )
    