from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы элементов главной страницы."""
    
    # Заголовки разделов
    TITLE_ASSEMBLE_BURGER = (
        By.XPATH, 
        "//h1[text()='Соберите бургер']"
    )
    
    SECTION_BUNS = (
        By.XPATH, 
        "//span[text()='Булки']/parent::div"
    )
    
    SECTION_SAUCES = (
        By.XPATH, 
        "//span[text()='Соусы']/parent::div"
    )
    
    SECTION_FILLINGS = (
        By.XPATH, 
        "//span[text()='Начинки']/parent::div"
    )
    
    # Кнопки
    LOGIN_BUTTON = (
        By.XPATH, 
        "//button[text()='Войти в аккаунт']"
    )
    
    CREATE_ORDER_BUTTON = (
        By.XPATH, 
        "//button[text()='Оформить заказ']"
    )
    
    # Ингредиенты (примеры)
    INGREDIENT_FLUORESCENT_BUN = (
        By.XPATH, 
        "//p[text()='Флюоресцентная булка R2-D3']/parent::a"
    )
    
    INGREDIENT_CRATER_BUN = (
        By.XPATH,
        "//p[text()='Краторная булка N-200i']/parent::a"
    )
    
    INGREDIENT_SPICY_SAUCE = (
        By.XPATH,
        "//p[text()='Соус Spicy-X']/parent::a"
    )
    
    # Счетчик ингредиента
    INGREDIENT_COUNTER = (
        By.XPATH,
        "//p[text()='Флюоресцентная булка R2-D3']/ancestor::a//p[@class='counter_counter__num__3nue1']"
    )
    
    # Конструктор (корзина)
    CONSTRUCTOR_AREA = (
        By.XPATH, 
        "//section[contains(@class, 'BurgerConstructor_basket')]//ul"
    )
    
    CONSTRUCTOR_BUN_TOP = (
        By.XPATH,
        "//span[contains(text(), 'верх')]"
    )
    
    CONSTRUCTOR_BUN_BOTTOM = (
        By.XPATH,
        "//span[contains(text(), 'низ')]"
    )
    
    # Модальное окно с деталями ингредиента
    INGREDIENT_DETAILS_TITLE = (
        By.XPATH, 
        "//h2[text()='Детали ингредиента']"
    )
    
    INGREDIENT_DETAILS_NAME = (
        By.XPATH,
        "//p[@class='text text_type_main-medium mb-8']"
    )
    
    INGREDIENT_DETAILS_CALORIES = (
        By.XPATH,
        "//p[text()='Калории,ккал']/following-sibling::p"
    )
    
    # Модальное окно с номером заказа
    ORDER_NUMBER_MODAL = (
        By.XPATH,
        "//h2[contains(@class, 'Modal_modal__title') and contains(@class, 'text_type_digits-large')]"
    )
    
    ORDER_IDENTIFIER_TEXT = (
        By.XPATH,
        "//p[text()='идентификатор заказа']"
    )
