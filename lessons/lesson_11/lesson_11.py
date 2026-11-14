# age = 22  # переменная


def say_hello():  # функция
    print("Hello")


class Dog:  # класс
    age_dog = 12  # атрибут

    def __init__(self, name):  # конструктор
        self.name = name

    def make_sound(self):  # метод
        print(f"{self.name}: 'гав-гав'")

dog = Dog("Boss")
dog_1 = Dog("Bob")
# print(id(dog))
# print(id(dog_1))
#
print(dog.name)
# print(dog_1.age_dog)
# print(dog_1.name)
# print(dog_1.make_sound())
# dog.make_sound()
# dog_1.make_sound()


# правила создания имен функций(или методов) и классов
# функций(или методов)
def get_device_id():  # snake_case
    pass

class AddEmployee:  # PascalCase
    pass

# camelCase


class Person:
    def __init__(self, name):
        self.name = name

    def greeting(self, age):
        if age < 5:
            return f"Я {self.name}, мне {age} года"
        elif age < 21:
            return f"Я {self.name}, мне {age} лет"
        else:
            return f"Я {self.name}, мне {age} год"

person_john_smith = Person("John")
print(person_john_smith.name)
print(person_john_smith.greeting(22))

person_2 = Person("Michael")
print(person_2.greeting(20))