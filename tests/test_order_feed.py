import allure
import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage


@allure.epic("UI Tests")
@allure.feature("Лента заказов")
class TestOrderFeed:
    """Тесты функциональности ленты заказов."""
    
    @allure.title("Увеличение счетчика 'Выполнено за все время' при создании заказа")
    @allure.description(
        "Проверка работы счетчика общего количества заказов.\n"
        "Шаги:\n"
        "1. Авторизоваться\n"
        "2. Перейти в ленту заказов и запомнить счетчик\n"
        "3. Создать новый заказ\n"
        "4. Вернуться в ленту и проверить увеличение счетчика"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_all_time_counter_increases(self, authorized_user):
        """Проверка увеличения счетчика за все время."""
        
        driver, email, password = authorized_user
        
        # Переходим в ленту заказов
        main_page = MainPage(driver)
        main_page.click_order_feed_button()
        
        # Запоминаем начальное значение счетчика
        order_feed_page = OrderFeedPage(driver)
        with allure.step("Получение начального значения счетчика"):
            initial_counter = order_feed_page.get_all_time_counter()
            allure.attach(
                str(initial_counter),
                name="Начальное значение счетчика",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Возвращаемся на главную и создаем заказ
        main_page.click_constructor_button()
        main_page.add_ingredient_to_constructor()
        main_page.click_create_order_button()
        
        # Получаем номер заказа для логирования
        with allure.step("Получение номера созданного заказа"):
            order_number = main_page.get_order_number()
            allure.attach(
                order_number,
                name="Номер заказа",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Закрываем модальное окно и переходим в ленту
        main_page.close_order_modal()
        main_page.click_order_feed_button()
        
        # Обновляем страницу для получения актуальных данных
        order_feed_page.refresh_page()
        
        # Получаем новое значение счетчика
        with allure.step("Получение нового значения счетчика"):
            new_counter = order_feed_page.get_all_time_counter()
            allure.attach(
                str(new_counter),
                name="Новое значение счетчика",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Проверяем увеличение
        with allure.step("Проверка увеличения счетчика"):
            assert new_counter > initial_counter, \
                f"Счетчик не увеличился. Было: {initial_counter}, Стало: {new_counter}"
            
            assert new_counter == initial_counter + 1, \
                f"Счетчик увеличился не на 1. Было: {initial_counter}, Стало: {new_counter}"
    
    @allure.title("Увеличение счетчика 'Выполнено за сегодня' при создании заказа")
    @allure.description(
        "Проверка работы счетчика заказов за сегодня.\n"
        "Шаги:\n"
        "1. Авторизоваться\n"
        "2. Перейти в ленту заказов и запомнить счетчик\n"
        "3. Создать новый заказ\n"
        "4. Вернуться в ленту и проверить увеличение счетчика"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_today_counter_increases(self, authorized_user):
        """Проверка увеличения счетчика за сегодня."""
        
        driver, email, password = authorized_user
        
        # Переходим в ленту заказов
        main_page = MainPage(driver)
        main_page.click_order_feed_button()
        
        # Запоминаем начальное значение счетчика
        order_feed_page = OrderFeedPage(driver)
        with allure.step("Получение начального значения счетчика"):
            initial_counter = order_feed_page.get_today_counter()
            allure.attach(
                str(initial_counter),
                name="Начальное значение счетчика за сегодня",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Создаем заказ
        main_page.click_constructor_button()
        main_page.add_ingredient_to_constructor()
        main_page.click_create_order_button()
        
        # Получаем номер заказа
        with allure.step("Получение номера созданного заказа"):
            order_number = main_page.get_order_number()
            allure.attach(
                order_number,
                name="Номер заказа",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Закрываем модальное окно и переходим в ленту
        main_page.close_order_modal()
        main_page.click_order_feed_button()
        
        # Обновляем страницу
        order_feed_page.refresh_page()
        
        # Получаем новое значение счетчика
        with allure.step("Получение нового значения счетчика"):
            new_counter = order_feed_page.get_today_counter()
            allure.attach(
                str(new_counter),
                name="Новое значение счетчика за сегодня",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Проверяем увеличение
        with allure.step("Проверка увеличения счетчика"):
            assert new_counter > initial_counter, \
                f"Счетчик не увеличился. Было: {initial_counter}, Стало: {new_counter}"
            
            assert new_counter == initial_counter + 1, \
                f"Счетчик увеличился не на 1. Было: {initial_counter}, Стало: {new_counter}"
    
    @allure.title("Появление номера заказа в разделе 'В работе'")
    @allure.description(
        "Проверка отображения заказа в разделе В работе.\n"
        "Шаги:\n"
        "1. Авторизоваться\n"
        "2. Создать новый заказ\n"
        "3. Перейти в ленту заказов\n"
        "4. Проверить наличие заказа в разделе 'В работе'"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_order_appears_in_progress(self, authorized_user):
        """Проверка появления заказа в разделе 'В работе'."""
        
        driver, email, password = authorized_user
        
        # Создаем заказ
        main_page = MainPage(driver)
        main_page.add_ingredient_to_constructor()
        main_page.click_create_order_button()
        
        # Получаем номер заказа
        with allure.step("Получение номера созданного заказа"):
            order_number = main_page.get_order_number()
            allure.attach(
                order_number,
                name="Номер заказа для проверки",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Закрываем модальное окно и переходим в ленту
        main_page.close_order_modal()
        main_page.click_order_feed_button()
        
        # Обновляем страницу для получения актуальных данных
        order_feed_page = OrderFeedPage(driver)
        order_feed_page.refresh_page()
        
        # Проверяем наличие заказа в разделе "В работе"
        with allure.step(f"Проверка наличия заказа #{order_number} в разделе 'В работе'"):
            # Получаем список всех заказов в работе для отладки
            orders_in_progress = order_feed_page.get_orders_in_progress()
            allure.attach(
                str(orders_in_progress),
                name="Все заказы в работе",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем наличие нашего заказа
            is_found = order_feed_page.is_order_in_progress(order_number)
            
            assert is_found, \
                f"Заказ #{order_number} не найден в разделе 'В работе'. " \
                f"Доступные заказы: {orders_in_progress}"
            