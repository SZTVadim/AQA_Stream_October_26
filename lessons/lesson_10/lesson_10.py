# Функции и условные контрукции в Python

a = 1

def circle_area(radius):
    PI = 3.14
    result = PI * radius * radius
    return result
    print(PI)


b = circle_area(1)
# print(b)

c = 1
f = 3
# print(b)
# n = circle_area(2)

def add(aa, bb, cc=0):
    print(f"aa : {aa}")
    print(f"bb : {bb}")
    print(f"cc : {cc}")
    return aa + bb + cc

# print(add(1, 2))
# print(add(bb=2, aa=3))
# print(add(bb=2, 3))  # SyntaxError: positional argument follows keyword argument
# print(add(2, bb=3, cc=5))

def sum_all(*args):
    return sum([n for n in args])

# print(sum_all(*[e for e in range(1, 100000)]))

# Условия
y = 15
def validation_int(num):
    if num % 2 == 0:
        print(f"{num} четное")
    else:
        print(f"{num} не четное")

# validation_int(1)
# validation_int(100)
# validation_int(999)

def new_validation_int(num):
    if num == 0:
        print(f"{num} ноль")
    elif num % 2 == 0:
        print(f"{num} четное")
    else:
        print(f"{num} не четное")


# new_validation_int(1)
# new_validation_int(0)
# new_validation_int(2)

# y = 0
# if y > 0:
#     print("положительное")
# elif y < 0:
#     print("отрицательное")
# else:
#     print("ноль")

# Условие в условии
x = 88
# if x >= 0:
#     if x < 10:
#         print(f"{x} цифра")
#     else:
#         print(f"{x} число")

# a, b, c, *_ = [1, 2, 3, 4, 5, 6, 7]
# print(a, b, c)
# print(_)

# match / case

def option_var(command):
    match command:
        case "start":
            print("Стартуем")
        case "stop":
            print("Останавливаем")
        case "pause":
            print("Пауза")
        case _:  # "_:" во всех остальных случаях, если другие кейсы дали false
            print("Неизвестная команда")

# option_var("any_option")
# def funny_option():
#     x = int(input("Введите число: "))
#     while x != 5:
#         print("Вы не угадали")
#         x = int(input("Введите число: "))
#     print("Вы угадали")
#
# funny_option()

# number = 1
# while number < 5:
#     print(f"number = {number}")
#     number += 1
# print("Работа программы завершена")

# циклы for
# else в for
message = "Hello"
def without_err():
    for l in message:
        print(l)
    else:
        print(f"Последний символ {l}. Цикл завершен")
    print("Работа программы завершена")

def with_err():
    for l in message:
        if l != "o":
            print(l)
        else:
            print("нашли 'o'")
            break
    else:
        print(f"Последний символ {l}. Цикл завершен")
    print("Работа программы завершена")

# without_err()
# with_err()

# Анонимные функции (lambda)
square = lambda x: x ** 3

print(square(5))

words = ["appleeee", "banana", "cherrry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)