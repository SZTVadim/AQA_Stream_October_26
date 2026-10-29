
# пример f-стринг
def greeting_name(name):
    print(f"Hello, {name}!")

greeting_name("Ivan")


# Что такое словари (dictionaries)
my_list = [1, 2, 3, 4, 5]
a = my_list.pop(1)
# print(my_list)

student = {
    "name": "Ivan",
    "age": 21,
    "is_teacher": False,
    "is_student": True,
    "address": {
        "city": [{"name": "Saratov", "street": "Leningradskaya st"},
                 {"name": "Tver", "street": "Sovetskaya st"}],
        "country": "Russia"
    }
}

# print(student["name"])
# print(student["address"]["country"])
# print(student["address"]["city"])
# print(student["address"]["city"][0]["street"])

# print(student.values())
# print(student.keys())
# print(student.items())

# Удаление элементов
student_new = {"имя": "Иван", "возраст": 20, "курс": 2}
# print(student_new)
# del student_new["курс"]
# print(student_new)
# age = student_new.pop("возраст")
# print(age)
# print(student_new)
student_new.clear()
# print(student_new)

# Добавление элементов
student_new["город"] = "Барнаул"
student_new["город1"] = "Калининград"
# print(student_new)


dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
dict1.update(dict2)
# print(dict1)

# Генераторы словарей (Dictionary Comprehensions)
# Создание словаря из списка:
square_dict = {f"элемент_{x}": x ** 2 for x in range(1, 6)}
print(square_dict)

# Фильтрация элементов:
square_dict_filter = {f"элемент_{x}": x ** 2 for x in range(1, 6) if x % 2 == 0}
print(square_dict_filter)

# Преобразование строкового ключа:
words = ["apple", "banana", "cherry"]
lenght_dict = {w: len(w) for w in words}
print(lenght_dict)

users = {"data":[
    {
        "id": 1,
        "name": "Анна",
        "is_admin": None,
        "profile": {
            "city": "Москва",
            "skills": ["Python", "pytest"],
            "settings": [{
                "theme": "dark",
                "notifications": True,
            }],
        },
    },
    {
        "id": 2,
        "name": "Борис",
        "is_admin": True,
        "profile": {
            "city": ["Казань", "СПБ", "Москва"],
            "skills": ["Java", "Selenium"],
            "settings": {
                "theme": "light",
                "notifications": False,
            },
        },
    },
]}

print(users["data"][0]["name"])
print(users["data"][1]["profile"]["settings"]["theme"])
print(users["data"][0]["profile"]["settings"][0]["theme"])
