# import uuid
#
# text = "Hello wjehf uwehfojcwdnejcbkjwebc kjweb kjwebc w"
# my_number = 5
#
# print(type(text))
# print(type(my_number))
# my_uuid = "02ef170c-ce8b-425f-99be-aafc0b235fb0"
# print(my_uuid.upper())
# print(type("02ef170c-ce8b-425f-99be-aafc0b235fb0".upper()))
# print(id(my_uuid))
#
#
# def func_hello():
#     print("Hello")
#
#
# func_hello()
#
# print("5" + "3")
# print(5 + 3)
# # result =  "5" + 3
#
# # Основные операции со строками - Преобразование регистра
# first_var = "heLLo worLD"
# print("=" * 30)
# print(id(first_var))
# # first_var = "hellO"
# # print(id(first_var))
#
# print(id(first_var.lower()))
# print(id(first_var.upper()))
# print(id(first_var.capitalize()))
# print(id(first_var.title()))


# Основные операции со строками - Удаление пробелов
# var_with_space = "  any text  "
# print(var_with_space)
# print(var_with_space.strip())
# print(var_with_space.lstrip())
# print(var_with_space.rstrip())
# var_with_int = "_a__any text___"
# print(var_with_int)
# print(var_with_int.strip("_"))

# Основные операции со строками - Разделение и объединение строк
# text = "яблоко,банан,апельсин"
# fruits = text.split(",")
# print(fruits)
# new_text = " | ".join(fruits)
# print(new_text)

# Основные операции со строками - Замена подстрок
# replace_text = "Я люблю java. java - это круто!"
# print(replace_text)
# new_text = replace_text.replace("java", "Python")
# print(new_text)

# Основные операции со строками - Поиск и подсчет
text_search_count = "Python программирование на Python"
# print(text_search_count.find("а"))
# print(text_search_count.find("ff"))
# print(text_search_count.index("на"))  # считает индекс первого вхождения, но если ничего не будет найдено, то упадет с ValueError
# print(text_search_count.count("Python"))
# print(text_search_count.count("Pytthon"))

# Основные операции со строками - Проверка типа символов
# print("Hello".isalpha()) # True
# print("123".isdigit())  # True
# print("Hello123".isalnum())  # True
# print("Hello".isalnum())  # True
# print("1234".isalnum())  # True
# print("   ".isspace())  # True
# print("".isspace())  # False

# Основные операции со строками - Преобразование между строками и числами
# age_str = "25"
# age = int(age_str)
# print(age + 5)
#
# price = 99.99
# price_str = str(price)
# print("Цена: " + price_str)

# Основные операции со строками - Срезы строк
# text = "Python"
# print(text[0:4])
# print(text[:3])
# print(text[3:])
# print(text[-4:])
# print(text[::2])

# Основные операции со строками - Переворот строки
# text = "nohtyP"
# reversed_test = text[::-1]
# print(reversed_test)
# Основные операции со строками - Экранирование символов
# print("Он сказал: \"Привет\"")
# print("first line\nSecond line")
# print("first line\tSecond line")

# Основные операции со строками - Тройные кавычки
text = """Это
многострочный
текст"""

print(text)