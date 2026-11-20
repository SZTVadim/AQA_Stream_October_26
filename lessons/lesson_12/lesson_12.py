# Задание 1: Класс для тестовых данных пользователя
# Задача:
# Создайте класс TestUser для хранения и работы с данными пользователя в тестах. Класс должен
# позволять создавать пользователей с различными данными и валидировать их корректность.

# Требования:
# 1. Класс должен иметь конструктор __init__, который принимает:
#    - username (обязательный)
#    - email (обязательный)
#    - password (обязательный)
#    - age (опциональный, по умолчанию None)
#    - is_active (опциональный, по умолчанию True)

# 2. Добавьте метод validate_email(), который проверяет, что email содержит символ "@"
#    и возвращает True/False

# 3. Добавьте метод validate_password(), который проверяет, что пароль содержит минимум
#   8 символов и возвращает True/False

# 4. Добавьте метод get_user_info(), который возвращает словарь со всеми данными пользователя


class TestUser:
    def __init__(self, username: str, email: str, password, age=None, is_active=True):
        self.username = username
        self.email = email
        self.password = password
        self.age = age
        self.is_active = is_active

    def validate_email(self):
        if "@" in self.email:
            return True
        else:
            return False
        # return "@" in self.email  # можно использовать аналоичное решение

    def validate_password(self):
        return len(self.password) >= 8


    def get_user_info(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "age": self.age,
            "is_active": self.is_active
        }

# 5. Добавьте метод is_adult(), который возвращает True, если возраст >= 18, иначе False
#    (если возраст не указан, возвращает None)

    def is_adult(self):
        if self.age is None:
            return None
        elif self.age >= 18:
            return True
        else:
            return False

        # if self.age is None:
        #     return None
        # return self.age >= 18

test_user_1 = TestUser(username="Anton", email="test@test.ru", password="12345", age=25)
print(test_user_1.validate_email())
print(test_user_1.password)
data = test_user_1.get_user_info()
print(data)
print(test_user_1.is_adult())
data["age"] = 17
print(data)
print(test_user_1.age)
test_user_1.age = 18
print(test_user_1.age)
