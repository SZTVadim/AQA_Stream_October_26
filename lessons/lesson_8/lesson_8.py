# Распаковка данных в Python

# Распаковка списка
# my_list = [1, 2]
# first = my_list[0]
# second = my_list[1]

# f, s = my_list

# new_list = [1, 2, 3]
# one, *two_three = new_list
# print(one)
# print(two_three)

# Распаковка кортежа
my_tuple = (1, 2, 3)
first = my_tuple[0]
second = my_tuple[1]
# print(first)
# print(second)

f, *s = my_tuple
# print(f)
# print(s)

# Распаковка множества (лучше не использовать из-за непредсказуемости)
# можно распаковать множество, но лучше преобразовать в другий тип данных
my_set = {"1", "2", "3"}
s_f, *s_s = my_set
# print(s_f)
# print(s_s)

# Распаковка словарей
student = {"name": "Иван", "age": 20, "city": "Москва"}
# for k, v in student.items():
    # print(k, v)

def greet(name, age, city):
    print(f"Привет, {name}! Тебе {age} лет. Ты из города {city}")

greet(name="Иван", age=20, city="Москва")
# greet(name=student["name"], age=student["age"], city=student["city"])
# greet(**student)

# *args и **kwargs
# Позиционные агументы
# greet("Ivan", 55, "Tver")

#. Именованные аргументы
# greet(name="Иван", age=20, city="Москва")

def process_data(*args, **kwargs):
    print("Позиционные аргументы: ", args)
    print("Именованные аргументы: ", kwargs)

    print(f"Всего позиционных аргументов: {len(args)}")
    print(f"Всего именованных аргументов: {len(kwargs)}")

process_data(1, 2, 4, name="Иван", age=20, city="Москва")

# student.update({"b": 123})
print(student)
new_student = student | {"b": 123}
print(new_student)
second_new_student = {**student, **new_student}
print(second_new_student)