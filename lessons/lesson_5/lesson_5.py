# Списки
a = 1
# В списках можем хранить различные типы данных
# list_int = [1, 2, 3]
# list_float = [1.1, 2.2, 3.3]
# list_str = ["a", "b", "c"]
# list_bool = [True, False, True]
# list_in_list = [[1, "1"], [2, [3, 4, 5, 6]]]
# list_dict = {"a": 1, "b": 2, "c": 3}
# list_int.remove(222)

# Добавление элементов
my_list = [1, 2, 3, "4"]
# my_list.append([4, 5, 6])  # пример ошибки при добавлении одного списка в другой
my_list.extend([4, 5, 6])
# print(my_list)
my_list.insert(1, 7)
my_list.insert(5, 7)
# print(my_list)

# Удаление элементов
# list_int.remove(222)  # пример который вызовет ValueError
my_list.remove(7)
# print(my_list)
my_list.pop(3)
my_var = my_list.pop()
# print(my_var)
# print(my_list)

# Поиск элементов
# fruits = ["яблоко", "банан", "апельсин", "банан"]
# print(fruits.index("банан"))  # возвращает индекс искомого элемента
# print(fruits.index(1))  # поулчим ошибку так как элемент не найден
# print(fruits.count("банан"))

# Сортировка и реверс
numbers = [3, 1, 4, 1, 5, 9, 2.33]
# numbers = ["аа", "a", "b", "c", "бб"]
numbers.reverse()
new_numbers = sorted(numbers)
# print(new_numbers)
# print(numbers)

# numbers.sort()
# print(numbers)
# numbers.sort(reverse=True)
# print(numbers)

# Минимум и максимум
# print(min(numbers))
# print(max(numbers))

# Копирование списков
original = [1, 2, 3]
a_list = original
copy_1 = original.copy()
copy_2 = original[:]
# print(id(original))
# print(id(copy_1))
# print(id(copy_2))
# print(id(a_list))

# Сумма элементов списка
print(sum(numbers))

# Генераторы списков (List Comprehensions)
squares = [x ** 3  for x in range(5, 10)]
print(squares)

words = ["helLLo", "WORLDD", "Apple"]
lower_case = [x.lower() for x in words]
print(lower_case)

# Генераторы списков (List Comprehensions) c if

my_words = ["cat", "dog", "elephant", "ant", "tiger"]
long_words = [w.upper() for w in my_words if len(w) > 5 ]
print(long_words)

# Генераторы списков (List Comprehensions) c if-else
long_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result_list = ["не четное" if x % 2 != 0 else "четное" for x in long_numbers]
print(result_list)
