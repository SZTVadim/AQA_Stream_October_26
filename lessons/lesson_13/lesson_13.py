# Абстракция в ООП

from abc import ABC, abstractmethod


class Car(ABC):
    @abstractmethod
    def start_engine(self):
        pass

    def stop_engine(self):
        print("Двигатель заглушен")


class GasolineCar(Car):
    a = 1

    def start_engine(self):
        print("Громкий рев двигателя")


class ElectricCar(Car):
    b = 2

    def start_engine(self):
        print("Безшумный старт двигателя")


# car_g = GasolineCar()
# car_g.start_engine()
# car_g.stop_engine()


# car_e = ElectricCar()
# car_e.start_engine()
# car_e.stop_engine()

# Инкапсуляция в ООП
class Кофемашина:
    def нагреть_воду(self):
        print("Нагреть воду")

    def помолоть_зерна(self):
        print("Мелю зерна...")

    def сварить_кофе(self):
        print("Варю кофе...")

    def варка(self):
        self.нагреть_воду()
        self.помолоть_зерна()
        self.сварить_кофе()

    def сделать_кофе(self):
        self.варка()
        return "Готовый кофе"

    def сделать_кофе_с_молоком(self):
        self.варка()
        print("Добавляем молоко")
        return "Готовый кофе с молоком"


# кофемашина = Кофемашина()
# print(кофемашина.сделать_кофе_с_молоком())
# print("=" * 30)
# print(кофемашина.сделать_кофе())


class BancAccount:
    def __init__(self, initial_balance=0):
        # __balance - приватное поле (скрыто от прямого доступа)
        self.__balance = initial_balance

    # Публичные методы - интерфейс для взаимодействия
    def deposit(self, deposit_amount):
        if deposit_amount > 0:
            self.__balance += deposit_amount
            return f"Пополнение: +{deposit_amount} руб."
        else:
            return "Сумма должна быть положительной"

    def withdraw(self, withdraw_amount):
        if withdraw_amount > 0:
            self.__balance -= withdraw_amount
            return f"Снятие: -{withdraw_amount} руб."
        else:
            return "Недостаточно средств или неверная сумма"

    def get_balance(self):
        return self.__balance


# account = BancAccount()
# print(account.get_balance())
# account.deposit(1000)
# print(account.get_balance())
# account.withdraw(999)
# print(account.get_balance())

# Наследование в ООП
class AnyCar:
    def __init__(self, brand, model, speed=0):
        self.brand = brand
        self.model = model
        self.speed = speed


class NewElectricCar(AnyCar):
    def __init__(self, brand, model, battery_level, speed=0):
        super().__init__(brand, model, speed)
        self.battery_level = battery_level  # Уровень заряда батареи

    def charge(self, amount):
        self.battery_level = min(100, self.battery_level + amount)
        print(f"Батарея заряжена до {self.battery_level}%")

    def display_info(self):
        # Переопределение метода для вывода дополнительной информации
        print(f"Электромобиль: {self.brand} {self.model}, Скорость: {self.speed} км/ч. Заряд: {self.battery_level} % ")


# Создание объекта класса ElectricCar:
# e_car = NewElectricCar("Tesla", "Model 3", battery_level=50)
# e_car.charge(30)
# e_car.display_info()

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Гав-гав!"


class Cat(Animal):
    def make_sound(self):
        return "Мяу!"


class Cow(Animal):
    def make_sound(self):
        return "Мууу!"


def sound_obj(animal: Animal):
    return animal.make_sound()


dog = Dog()
cat = Cat()
cow = Cow()

# print(dog.make_sound())
# print(cat.make_sound())
# print(cow.make_sound())


print(sound_obj(dog))
print(sound_obj(cat))
print(sound_obj(cow))
