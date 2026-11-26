# Декораторы
# Простой декоратор
import time


def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Начало выполнения функции")
        func(*args, **kwargs)
        print("Конец выполнения функции")

    return wrapper


@my_decorator
def greet(name):
    print(f"Hello {name}")


# greet("Gena")

a = 1


# Параметризованный декоратор

def my_repeat_decorator(count_repeat):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(count_repeat):
                func(*args, **kwargs)

        return wrapper

    return decorator


@my_repeat_decorator(count_repeat=3)
def new_greet(name):
    print(f"Hello {name}")


# new_greet("Gena")


def мой_декоратор(функция):
    def обертка():
        print("Начинаем работу...")  # Действие ДО основной функции
        функция()  # Вызываем саму функцию
        print("Завершаем работу.")  # Действие ПОСЛЕ основной функции

    return обертка


# Создаем обычную функцию
def _сказать_привет():
    print("Привет, мир!")


# Применяем декоратора, которую мы используем как обычную функцию(лучше так не делать)
сказать_привет = мой_декоратор(_сказать_привет)


# Вызываем саму функцию
# сказать_привет()


# Реальный пример декоратора
def duration_func(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()

        print(f"Функция выполнялась {end_time - start_time :.3} секунд")
        """ ':.3' указывает до скольки знаков после запятой необходимо округлить, в результате будет3.11"""

    return wrapper


@duration_func
def func_awaiting(any_time):
    print("Выполняю сложные вычисления...")
    time.sleep(any_time)


# func_awaiting(3.11223423423432)

# Метод класса( @classmethod)

class Car:
    car_count = 0

    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        Car.car_count += 1

    @classmethod
    def from_str(cls, car_str):
        brand, model = car_str.split("-")
        return cls(brand, model)


car1 = Car.from_str("Ford-Focus")
car2 = Car.from_str("Toyota-Corolla")


# print(f"Бренд: {car1.brand}, Модель: {car1.model}")
# print(f"Всего автомобилей: {Car.car_count}")
#
# print(f"Бренд: {car2.brand}, Модель: {car2.model}")
# print(f"Всего автомобилей: {Car.car_count}")


class Employee:
    company = "TechCorp"  # Обычная переменная класса (общая для всех объектов)

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display_info(self):
        # Обычный метод - работает с конкретным объектом (self)
        print(f"{self.name} зарабатывает {self.salary} в компании {self.company}")

    @staticmethod
    def any_method():
        print(f"Hello")

    @classmethod
    def change_company(cls, new_company):
        # Метод класса - работает с классом в целом (cls)
        cls.company = new_company
        print(f"Название компании изменено на: {new_company}")

    @classmethod
    def from_string(cls, employee_string):
        # Ещё один полезный пример - альтернативный конструктор
        name, salary = employee_string.split("-")
        return cls(name, int(salary))


# Создаем объекты
# emp1 = Employee("Иван", 50000)
# emp2 = Employee("Мария", 60000)
# print(emp1.salary)

# Используем обычный метод
# emp1.display_info()  # Иван зарабатывает 50000 в компании TechCorp

# Используем метод класса - меняем компанию для ВСЕХ объектов
# Employee.change_company("NewTech")

# Теперь все объекты используют новое название компании
# emp1.display_info()  # Иван зарабатывает 50000 в компании NewTech
# emp2.display_info()  # Мария зарабатывает 60000 в компании NewTech

# Используем альтернативный конструктор
# emp3 = Employee.from_string("Петр-70000")
# emp3.display_info()  # Петр зарабатывает 70000 в компании NewTech
#
# Employee.any_method()  # Правильное обращение к staticmethod
# emp1.any_method()  # НЕ правильное обращение к staticmethod

# Свойства класса (@property)
class NewCar:
    def __init__(self, brand, model, speed_car=0):
        self.brand = brand
        self.model = model
        self.__speed = speed_car  # Приватный атрибут скорости

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        if value < 0:
            print("Ошибка: скорость не может быть отрицательной!")
        elif value > 300:
            print("Ошибка: превышено максимально допустимое значение скорости (300 км/ч)!")
        else:
            self.__speed = value


new_car1 = NewCar("Toyota", "Corolla")
print(new_car1.speed)
new_car1.speed = 1001
print(new_car1.speed)
new_car1.speed = 300
print(new_car1.speed)
