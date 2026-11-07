# Ermolaenko_A
# Lesson 9 — индивидуальные задания

# ========== Часть 1 (задача 18) ==========
# Задача 18: Работа с bool
# Даны флаги:
is_auth = True
is_admin = False
# 1. Проверьте, что пользователь авторизован И админ
# 2. Проверьте, что пользователь авторизован ИЛИ админ
# 3. Инвертируйте is_admin 

# ========== Часть 2 (задача 2) ==========
# Задача 2:
response = {"status": 200, "data": {"token": "abc123", "expires_in": 3600}}
# Извлеките token и expires_in, сравните, больше ли expires_in нуля

print(is_auth and is_admin)
print(is_auth or is_admin)
print(not is_admin)

token = response["data"]["token"]
print(token)
expires_in = response["data"]["expires_in"]
print(expires_in)
print(expires_in > 0)