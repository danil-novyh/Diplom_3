import allure
import random
import string


class DataGenerator:
    """Класс для генерации случайных тестовых данных."""
    
    @staticmethod
    @allure.step("Генерация случайной строки длиной {length}")
    def generate_random_string(length=10):
        """
        Генерация случайной строки из букв.
        
        Args:
            length: Длина строки
            
        Returns:
            str: Случайная строка
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    @allure.step("Генерация случайного email")
    def generate_random_email():
        """
        Генерация случайного email адреса.
        
        Returns:
            str: Email адрес
        """
        username = DataGenerator.generate_random_string(8)
        domain = DataGenerator.generate_random_string(5)
        return f"{username}@{domain}.ru"
    
    @staticmethod
    @allure.step("Генерация случайного пароля")
    def generate_random_password(length=10):
        """
        Генерация случайного пароля.
        Содержит буквы и цифры.
        
        Args:
            length: Длина пароля
            
        Returns:
            str: Пароль
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    @allure.step("Генерация данных для регистрации пользователя")
    def generate_user_payload():
        """
        Генерация полного набора данных для регистрации.
        
        Returns:
            dict: Словарь с email, password, name
        """
        return {
            "email": DataGenerator.generate_random_email(),
            "password": DataGenerator.generate_random_password(),
            "name": DataGenerator.generate_random_string(8)
        }


class APIHelper:
    """Вспомогательные методы для работы с API."""
    
    @staticmethod
    @allure.step("Создание пользователя через API")
    def create_user(payload, config):
        """
        Создание пользователя через API.
        
        Args:
            payload: Данные пользователя
            config: Объект конфигурации с URL
            
        Returns:
            tuple: (access_token, refresh_token)
        """
        import requests
        
        response = requests.post(config.API_REGISTER, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("accessToken"), data.get("refreshToken")
        else:
            raise Exception(f"Failed to create user: {response.text}")
    
    @staticmethod
    @allure.step("Удаление пользователя через API")
    def delete_user(access_token, config):
        """
        Удаление пользователя через API.
        
        Args:
            access_token: Токен доступа
            config: Объект конфигурации с URL
        """
        import requests
        
        if access_token:
            headers = {"Authorization": access_token}
            response = requests.delete(config.API_USER, headers=headers)
            
            if response.status_code not in [200, 202]:
                print(f"Warning: Failed to delete user: {response.text}")
                