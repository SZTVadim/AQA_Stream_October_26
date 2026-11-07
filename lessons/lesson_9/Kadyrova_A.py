# Kadyrova_A
# Lesson 9 — индивидуальные задания

# ========== Часть 1 (задача 19) ==========
# Задача 19: Работа с bool
# Дан статус код и флаг:
#status_code = 200
#has_body = True
# Получите bool: успешен ли ответ?
# Условие: status_code == 200 и has_body == True

# ========== Часть 2 (задача 5) ==========
# Задача 5:
# Получите новый список только валидных email (условие: содержит "@" и ".").
# Замените последний элемент коллекции, исправив "," на "."
#emails = ["a@test.com", "bad-email", "b@site,org"]



#19
status_code = 200
has_body = True
print(200 <= status_code <= 299)
print(status_code == 200 and has_body == True)


#Задача 5
emails = ["a@test.com", "bad-email", "b@site,org"]
valid_emails = [e for e in emails if "@" in e and "." in e]
print(valid_emails)
emails[-1] = emails[-1].replace(",", ".")
print(emails)