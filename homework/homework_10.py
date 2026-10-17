"""
Темы: Распаковка данных
"""


# ЗАДАНИЕ 1: Распаковка списка и слияние
# Дан список статусов пайплайна:
# statuses = ["queued", "running", "testing", "deploy", "done"]
#
# 1. Распакуйте так, чтобы:
#    - first — первый элемент
#    - last — последний элемент
#    - middle — все средние элементы списком
# 2. Создайте новый список: объедините middle с ["failed", "skipped"] через распаковку *
# 3. Выведите first, last и новый список

# ЗАДАНИЕ 2: Словарь, слияние и вызов функции

# Дано:
# browser = {"browser": "chrome", "timeout": 3000}
# options = {"headless": True, "timeout": 5000}
#
# def start_session(browser, timeout, headless):
#     return f"{browser}, timeout={timeout}, headless={headless}"
#
# 1. Объедините browser и options в словарь config через {**..., **...}
# 2. Вызовите start_session, распаковав config через **
# 3. Выведите config и результат функции