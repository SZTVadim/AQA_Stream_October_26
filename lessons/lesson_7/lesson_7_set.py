# Множества - коллекции уникальных элементов

# numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
# print(numbers)
# new_numbers = {"1111", "2222", "3333", "4444", "5444", "6444", "4", "75", "845345", "934535"}
# print(new_numbers)
words = {"apple", "banana", "cherry", "strawberry"}
# print(words)

list_numbers = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
# print(set(list_numbers))
word = "hello world, it's beautiful day"
# print(set([w.strip(",") for w in word.split()]))

# Добавления элементов во множество
words.add("mango")
# print(words)
words.update(["груша", "виноград"])
# print(words)

# Удаление элементов
words.remove("mango")
# words.remove("mango"). # Вызовет ошибку,так как удаляемый элемент отсутствует
# print(words)
words.discard("виноград")
words.discard("виноград")
# print(words)
random_fruit = words.pop()
print(random_fruit)
print(words)


