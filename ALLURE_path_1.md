# Интеграция Allure Report в UI_project

Пошаговая инструкция: как подключить Allure к проекту (для примера использую UI проект с PW),

---

## 0. Что получим в итоге

- Прогон `pytest` пишет результаты в папку `allure-results/`
- Локально одной командой открываем красивый HTML-отчёт
- При повторных прогонах в отчёте видна **история** (графики Trend, Retries, Flaky)

---

## 1. Установка зависимостей Python

В окружении проекта (venv/PyCharm interpreter для нашего проекта):

```bash
pip install pytest playwright pytest-playwright allure-pytest
playwright install
```

Проверить, что всё встало:

```bash
pip show allure-pytest playwright pytest-playwright
```

Зафиксировать версии в `requirements.txt` (в корне репозитория):

```
pytest==7.4.3
playwright
pytest-playwright
allure-pytest
```
---

## 2. Установка Allure CLI (генератор отчёта)

`allure-pytest` только **пишет данные** прогона. Чтобы собрать из них HTML-отчёт, нужен
отдельный **Allure Commandline**, который требует Java.

### macOS

```bash
brew install allure
```

Проверка:

```bash
allure --version
java -version
```

Если `java` не установлен — см. раздел **2.1 Установка Java 21** ниже.

### Linux (для CI на self-hosted runner, если понадобится)

```bash
sudo apt update
sudo apt install -y default-jre
curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.tgz
sudo tar -zxvf allure.tgz -C /opt/
sudo ln -s /opt/allure-2.29.0/bin/allure /usr/bin/allure
```

---

## 2.1 Установка Java 21 (macOS и Windows)

Allure Commandline требует установленную Java. Ниже — установка **Java 21 (LTS)**.

### macOS

**Вариант 1: Homebrew (рекомендуется)**

```bash
brew install openjdk@21
```

После установки прописать в `PATH` (Homebrew подскажет команду, обычно такая):

```bash
echo 'export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Проверка:

```bash
java -version
```

Должно быть что-то вроде:

```
openjdk version "21.0.x"
```

**Вариант 2: скачать вручную**

1. Открыть [https://adoptium.net](https://adoptium.net)
2. Выбрать **Temurin 21 (LTS)** → **macOS** → `.pkg`
3. Установить как обычное приложение
4. Проверить: `java -version`

### Windows

**Вариант 1: winget (Windows 10/11, рекомендуется)**

В PowerShell или CMD:

```powershell
winget install EclipseAdoptium.Temurin.21.JDK
```

Перезапустить терминал, проверить:

```powershell
java -version
```

**Вариант 2: скачать вручную**

1. Открыть [https://adoptium.net](https://adoptium.net)
2. Выбрать **Temurin 21 (LTS)** → **Windows** → `.msi`
3. Запустить установщик — **обязательно отметить** галочки **"Set JAVA_HOME variable"** и **"Add to PATH"**
4. Перезапустить терминал/PyCharm
5. Проверить:

```powershell
java -version
echo $env:JAVA_HOME     # PowerShell
```

**Если `JAVA_HOME` не подхватился:**

```powershell
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-21.x.x-hotspot"
setx PATH "%PATH%;%JAVA_HOME%\bin"
```

### Проверка перед запуском Allure (обе ОС)

```bash
java -version
allure --version
```

Если `allure` не видит Java — обычно проблема именно в `JAVA_HOME`/`PATH`, а не в самом Allure.

---

## 3. Запуск тестов с Allure через командную строку

Самый простой способ понять, что делает Allure — сначала прогнать тесты
**без всякого конфига**, вручную указывая флаги в терминале.

Из корня репозитория:

```bash
pytest test --alluredir=allure-results
```

Разбор флагов:

- `test` — где искать тесты
- `--alluredir=allure-results` — куда писать результаты прогона (`.json` файлы по каждому тесту) — это данные для будущего Allure-отчёта

Если хочешь, чтобы перед каждым новым прогоном папка с результатами очищалась
(иначе старые и новые результаты будут копиться вместе), добавь ещё один флаг:

```bash
pytest UI_project/test --alluredir=allure-results --clean-alluredir
```

После прогона в папке `allure-results/` появятся файлы вида:

```
allure-results/
├── 1234abcd-result.json
├── 1234abcd-container.json
├── environment.properties   (если добавишь, см. ниже)
```

Это и есть «данные текущего прогона» — их использует Allure CLI для генерации отчёта.

### Посмотреть отчёт локально (самый быстрый способ)

```bash
allure serve allure-results
```

Команда сама поднимет временный сервер и откроет отчёт в браузере.

### Сгенерировать статический отчёт (для CI / сохранения)

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Добавить `allure-results/` и `allure-report/` в `.gitignore`, чтобы эти папки
не попадали в git:

```
allure-results/
allure-report/
```

---

## 4. `pytest.ini` — чтобы не писать флаги каждый раз

Постоянно набирать `--alluredir=allure-results --clean-alluredir` в терминале
неудобно. Чтобы pytest подставлял эти флаги **автоматически**, создаём в
корне репозитория файл `pytest.ini`:

```ini
[pytest]
addopts = --alluredir=allure-results --clean-alluredir
```

Что делает каждая строка:

- `addopts = --alluredir=allure-results --clean-alluredir` — pytest сам подставит эти флаги при каждом запуске:
  - `--alluredir=allure-results` — пишет результаты каждого теста (JSON-файлы) в папку `allure-results/`
  - `--clean-alluredir` — перед запуском очищает `allure-results/`, чтобы туда не попадали результаты от предыдущих прогонов вперемешку с новыми

После того как файл создан, вместо

```bash
pytest test --alluredir=allure-results --clean-alluredir
```

достаточно просто:

```bash
pytest
```

pytest сам найдёт `pytest.ini` в корне репозитория и подставит все настройки.

---

## 5. Как размечать тесты Allure-декораторами (памятка)

Используются прямо в файлах `UI_project/test/*.py`. Пример на основе твоего
`test_authorize.py`:

```python
import allure

@allure.epic("UI OrangeHRM")
@allure.feature("Authorization")
class TestAuthorize:

    @allure.title("Успешная авторизация пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_authorize(self, auth_page, dashboard_page):
        with allure.step("Авторизоваться валидными данными"):
            auth_page.authorize(USERNAME, PASSWORD)

        with allure.step("Проверить, что открылся Dashboard"):
            expect(dashboard_page.page).to_have_url(dashboard_page.full_url(dashboard_page.PAGE_URL))
```

Полезные декораторы:

| Декоратор | Зачем |
|---|---|
| `@allure.title("...")` | человекочитаемое название теста в отчёте |
| `@allure.step("...")` | шаг внутри теста (можно вкладывать) |
| `@allure.severity(...)` | важность (BLOCKER/CRITICAL/NORMAL/MINOR/TRIVIAL) |
| `@allure.feature("...")` / `@allure.epic("...")` | группировка в отчёте (Behaviors) |
| `allure.attach(...)` | приложить скриншот/лог/json к тесту |

### Автоскриншот при падении теста (полезно для UI)

В `conftest.py` (`test/conftest.py`):

```python
import allure
import pytest

@pytest.fixture
def page(context, request):
    page = context.new_page()
    yield page
    if request.node.rep_call.failed:
        allure.attach(page.screenshot(), name="failure", attachment_type=allure.attachment_type.PNG)
```

Для `request.node.rep_call` нужен стандартный хук в `conftest.py`:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
```

---

## Доп. материал A — Настройка истории прогонов (Trend/Retries/Flaky)

По умолчанию **каждый** `allure generate` создаёт отчёт «с нуля», без истории.
Чтобы видеть графики истории между прогонами, нужно переносить папку `history/`
из **предыдущего** отчёта в **новые** `allure-results` перед генерацией.

### Локально

```bash
# 1. Прогнать тесты (используются флаги из pytest.ini, см. раздел 4)
pytest

# 2. Перед генерацией скопировать историю из старого отчёта в свежие результаты
cp -r allure-report/history allure-results/history

# 3. Сгенерировать новый отчёт — Allure сам подхватит папку history
allure generate allure-results --clean -o allure-report
```

> Важно: копировать `history/` нужно **после** прогона тестов (шаг 1), но **до**
> генерации отчёта (шаг 3) — иначе `--clean-alluredir` из `pytest.ini` удалит
> скопированную историю вместе со старыми результатами.
> (Делаем прогон, копируем, генерируем)

Повторяя эти 3 шага из раза в раз, в отчёте появятся:
- **Trend** — график успешных/упавших тестов по прогонам
- **Retries** — если тест был нестабильным (flaky) и падал/проходил
- **History** — статус конкретного теста в предыдущих запусках
