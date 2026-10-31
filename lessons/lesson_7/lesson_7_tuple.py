# Кортежи
my_tuple = (1, 2, 3)
my_tuple_new = 1, 2, 3
# print(my_tuple)
# print(type(my_tuple))
# print(my_tuple_new)
# print(type(my_tuple_new))

# Основыне операции с кортежами
# print(my_tuple[-1])
# print(my_tuple[1:3])
# print(1 in my_tuple)
# print(55 in my_tuple)
# print(len(my_tuple))

my_new_tuple = my_tuple + my_tuple
# print(my_new_tuple)
my_new_tuple_1 = (1, 2) * 3
# print(my_new_tuple_1)

# поиск и подсчет
# print(my_tuple.index(3))
# print(my_tuple.index(32))  # такого элемента нет => ValueError
# print(my_new_tuple_1.count(3))
# print(my_new_tuple_1.count(1))

# Кортежи из одного элемента
single = 5,
# print(type(single))

# Использование кортежа как ключа для словаря(dict)
coord_work = (125, 160)
coord_home = (10, 20)
coord = {coord_work: "Работа", coord_home: "Дом"}
# Распаковка кортежей
point = (10, 20)
x, y = point

points = (1, 2, 3, 4, 5, 6)

xx, *yy = points
# print(f"xx: {xx}")
# print(f"yy: {yy}")

xx, yy = yy, xx
# print(f"xx: {xx}")
# print(f"yy: {yy}")
# print(x)
# print(y)

# print(coord.keys())
# print(coord.items())
# print(coord.values())

# print(hash(coord_home))
# print(hash(coord_work))
# print(hash([1, 2, 3]))

# Генераторы кортежей (Tuple Comprehensions)
generotor = (x for x in range(1, 6))
print(generotor)
print(type(generotor))
print(tuple(generotor))  # Чтобы получить именно кортеж, нужно обернуть генераторное выражение в функцию tuple()