"""
Домашнее задание 13
"""
#  Создайте класс TestCase:

# 1) В __init__ принимайте:
#    - name (название теста)
#    - status (по умолчанию "new")
#    - duration (время в секундах, по умолчанию None)
#
# 2) Метод can_run():
#    - возвращает True, только если status == "new"
#    - иначе False
#
# 3) Метод finish(result, duration):
#    - если тест нельзя запустить (can_run() == False) —
#      ничего не меняет и возвращает False
#    - если result не "passed" и не "failed" —
#      ничего не меняет и возвращает False
#    - иначе ставит status = result, duration = duration и возвращает True
#
# 4) Метод is_slow():
#    - если duration не указан (None) — вернуть None
#    - если duration >= 5 — True
#    - иначе False
#
# 5) Создайте 3 объекта:
#    - новый тест без duration
#    - тест, который успешно завершили через finish
#    - тест, у которого finish вызвали повторно или с неверным result
#    Выведите для каждого: name, can_run(), is_slow(), status