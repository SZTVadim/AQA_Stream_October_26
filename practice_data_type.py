import json

data = {"id": 101, "name": "Ivan", "role": "admin", "active": None}
print(data)
data_json= json.dumps(data)
print(data_json)


# Часть 2

# Задача 1: Извлечение данных из словаря
user = {"id": 101, "name": "Ivan", "role": "admin", "active": True}
# Извлеките name и role
name = user["name"]
role = user["role"]
# print(f"Роль: {role}, Имя: {name}")

# Задача 2:
response = {"status": 200, "data": {"token": "abc123", "expires_in": 3600}}
# Извлеките token и expires_in сравнитть больше ли 0
token = response["data"]["token"]
expires_in = response["data"]["expires_in"] > 0
# print(expires_in)

# Задача 3:
products = [{"id": 1, "name": "Phone"}, {"id": 2, "name": "Laptop"}]
product_laptop = products[1]["name"]
# print(product_laptop)

# Задача 4:
# Из списка чисел получите список квадратов только четных чисел через list comprehension
numbers = [1, 2, 3, 4, 5, 6]
square = [x ** 2 for x in numbers if x % 2 == 0]
# print(square)

# Задача 5:
# Получите новый список только валидных email (условие: содержит "@" и ".").
emails = ["a@test.com", "bad-email", "b@site,org"]
valid_email = [x for x in emails if "@" in x and "." in x]
# print(valid_email)

# Задача 6:
# Получите список имен пользователей старше 18.
users = [{"name": "Ann", "age": 20}, {"name": "Bob", "age": 17}, {"name": "Kate", "age": 25}]
user_over_18 = [x["name"] for x in users if x["age"] > 18]
# print(user_over_18)

# Задача 7:
# Создайте словарь только с endpoint, где код 200.
pairs = [("login", 200), ("profile", 404), ("orders", 200)]
pairs_new = {key: value for key, value in pairs if value == 200} 
# print(pairs_new)

# Задача 8:
# Дан список URL с дублями. Получите количество уникальных URL.
urls = ["/login", "/login", "/profile", "/orders", "/orders"]
unique_count = len(set(urls))
# print(unique_count)

# Задача 9:
# Даны множества ролей:
backend_roles = {"admin", "editor", "viewer"}
frontend_roles = {"viewer", "guest"}
# - пересечение,
# - только backend,
# - только frontend.
common_roles = backend_roles & frontend_roles
# print(common_roles)
backend_only = backend_roles - frontend_roles
# print(backend_only)
frontend_only = frontend_roles - backend_roles
# print(frontend_only)

# Задача 10:
# Дан список времени ответа API в мс:
timings = [120, 95, 305, 210, 98]
# Найдите min/max/avg, проверьте, что среднее < 200.
min_t = min(timings)
max_t = max(timings)
avg = sum(timings) / len(timings) < 200
# print(f"Min: {min_t}, Max: {max_t}, Avg: {avg}")

# Задача 11:
# Дан URL:
url = "https://site.com/api/v1/users?id=15"
# Проверьте, что URL содержит "/api/",
# и извлеките query-параметр id строковыми методами (без библиотек).
has_api = "/api/" in url 
# print(has_api)
query = url.split("?")[1]
# print(query)
user_id = query.split("=")[1]
# print(user_id)







# Начать с заданий 12
# Часть 1

# Задача 12: Работа со строкой
# Дана строка:
text = "  Status: OK  "
# 1. Уберите пробелы по краям
# 2. Переведите в нижний регистр
# 3. Проверьте, что строка заканчивается на "ok"
# Задача 13: Работа со строкой
# Дан email:
email = "Test.User@Example.COM"
# 1. Приведите email к нижнему регистру
# 2. Разделите на имя и домен по "@"
# 3. Выведите имя и домен отдельно
# Задача 14: Работа с числами (int)
# Даны два числа:
a = 17
b = 5
# Найдите:
# 1. сумму
# 2. частное (обычное деление)
# 3. целую часть от деления
# 4. остаток от деления
# Задача 15: Работа с числами (int)
# Дан номер теста:
test_id = 42
# 1. Проверьте, что test_id чётный
# 2. Проверьте, что test_id находится в диапазоне от 1 до 100 включительно
# Задача 16: Работа с float
# Дана цена:
price = 19.99
# 1. Посчитайте цену с НДС 20% (price * 1.2)
# 2. Округлите результат до 2 знаков после запятой (round)
# 3. Преобразуйте округлённую цену в int
# Задача 17: Работа с float
# Дано время ответа API:
response_time = 0.357
# 1. Переведите в миллисекунды (* 1000)
# 2. Округлите до целого
# 3. Проверьте, что результат < 500
# Задача 18: Работа с bool
# Даны флаги:
is_auth = True
is_admin = False
# 1. Проверьте, что пользователь авторизован И админ
# 2. Проверьте, что пользователь авторизован ИЛИ админ
# 3. Инвертируйте is_admin (not)
# Задача 19: Работа с bool
# Дан статус код и флаг:
status_code = 200
has_body = True
# Получите bool: успешен ли ответ?
# Условие: status_code == 200 и has_body == True
# Задача 20: Смешанная (str + int)
# Дана строка с числом:
value = "150"
# 1. Преобразуйте в int
# 2. Умножьте на 2
# 3. Преобразуйте результат обратно в str
# Задача 21: Смешанная (str + float + bool)
# Дан текст:
message = "error: timeout after 2.5 sec"
# 1. Проверьте, что в тексте есть слово "error" (bool)
# 2. Извлеките число 2.5 из строки и преобразуйте в float
#    (подсказка: split)