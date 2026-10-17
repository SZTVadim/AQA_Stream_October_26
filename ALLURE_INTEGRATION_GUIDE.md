# Интеграция Allure Report в UI_project

Пошаговая инструкция: как подключить Allure к `UI_project` (pytest + Playwright),
получить отчёт по текущему прогону, настроить историю прогонов и подключить всё
в CI (GitHub Actions и Jenkins).

Текст шагов (`@allure.step`, `@allure.title` и т.д.) внутри тестов ты пишешь сам —
здесь описана только последовательность **настройки и интеграции**.

---

## 0. Что получим в итоге

- Прогон `pytest` пишет результаты в папку `allure-results/`
- Локально одной командой открываем красивый HTML-отчёт
- При повторных прогонах в отчёте видна **история** (графики Trend, Retries, Flaky)
- Отчёт публикуется автоматически в **GitHub Actions**
- Отчёт публикуется автоматически в **Jenkins** (с историей между билдами)

---



## 1. Установка зависимостей Python

В окружении проекта (venv/PyCharm interpreter для `UI_project`):

```bash
pip install pytest playwright pytest-playwright allure-pytest
playwright install
```

Проверить, что всё встало:

```bash
pip show allure-pytest playwright pytest-playwright
```

Зафиксировать версии в `requirements.txt` (в корне репозитория или в `UI_project`):

```
pytest==7.4.3
playwright
pytest-playwright
allure-pytest
```

> В твоём окружении `allure-pytest` уже установлен — проверено. Осталось доустановить `playwright` / `pytest-playwright`, если их ещё нет в реальном venv, который использует PyCharm.

---



## 2. Установка Allure CLI (генератор отчёта)

`allure-pytest` только **пишет данные** прогона. Чтобы собрать из них HTML-отчёт, нужен
отдельный **Allure Commandline**, который требует Java.

### macOS (у тебя darwin)

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

**Если** `JAVA_HOME` **не подхватился:**

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
pytest UI_project/test --alluredir=allure-results
```

Разбор флагов:

- `UI_project/test` — где искать тесты
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
testpaths = UI_project/test
```

Что делает каждая строка:

- `addopts = --alluredir=allure-results --clean-alluredir` — pytest сам подставит эти флаги при каждом запуске:
  - `--alluredir=allure-results` — пишет результаты каждого теста (JSON-файлы) в папку `allure-results/`
  - `--clean-alluredir` — перед запуском очищает `allure-results/`, чтобы туда не попадали результаты от предыдущих прогонов вперемешку с новыми
- `testpaths = UI_project/test` — где искать тесты по умолчанию (не нужно писать путь в команде)

После того как файл создан, вместо

```bash
pytest UI_project/test --alluredir=allure-results --clean-alluredir
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


| Декоратор                                        | Зачем                                            |
| ------------------------------------------------ | ------------------------------------------------ |
| `@allure.title("...")`                           | человекочитаемое название теста в отчёте         |
| `@allure.step("...")`                            | шаг внутри теста (можно вкладывать)              |
| `@allure.severity(...)`                          | важность (BLOCKER/CRITICAL/NORMAL/MINOR/TRIVIAL) |
| `@allure.feature("...")` / `@allure.epic("...")` | группировка в отчёте (Behaviors)                 |
| `allure.attach(...)`                             | приложить скриншот/лог/json к тесту              |




### Автоскриншот при падении теста (полезно для UI)

В `conftest.py` (`UI_project/test/conftest.py`):

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

Повторяя эти 3 шага из раза в раз, в отчёте появятся:

- **Trend** — график успешных/упавших тестов по прогонам
- **Retries** — если тест был нестабильным (flaky) и падал/проходил
- **History** — статус конкретного теста в предыдущих запусках



### В CI (общая идея, детали ниже по каждой системе)

История должна **сохраняться между запусками CI**, поэтому:

- в GitHub Actions — публикуем каждый отчёт на `gh-pages` и перед генерацией скачиваем `history/` из уже опубликованного отчёта;
- в Jenkins — используется плагин Allure, который **сам** хранит историю по номерам билдов (ничего вручную копировать не нужно).



### `environment.properties` (доп. инфо в отчёте: окружение, браузер, версия)

Создать файл `allure-results/environment.properties` перед генерацией (можно генерировать скриптом в CI):

```properties
Browser=Chromium
Environment=Staging
Python.Version=3.13
Base.URL=https://opensource-demo.orangehrmlive.com
```

Allure покажет это на вкладке **Environment** в отчёте.

---



## Доп. материал B — Интеграция в CI через GitHub Actions

В репозитории уже есть `.github/workflows/lint.yml` — добавляем **отдельный** workflow
для тестов + Allure, например `.github/workflows/tests.yml`:

```yaml
name: UI Tests with Allure Report

on:
  push:
    branches: [ "**" ]
  pull_request:
    branches: [ "**" ]

permissions:
  contents: write   # нужно, чтобы пушить отчёт в gh-pages

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest playwright pytest-playwright allure-pytest
          playwright install --with-deps chromium

      - name: Run UI tests
        run: |
          pytest UI_project/test --alluredir=allure-results
        continue-on-error: true   # чтобы отчёт собрался даже при упавших тестах

      - name: Load previous Allure history (для Trend)
        uses: actions/checkout@v4
        with:
          ref: gh-pages
          path: gh-pages
        continue-on-error: true

      - name: Copy history into results
        run: |
          mkdir -p allure-results/history
          cp -r gh-pages/history/* allure-results/history/ 2>/dev/null || true

      - name: Generate Allure report
        uses: simple-elf/allure-report-action@master
        with:
          allure_results: allure-results
          allure_history: allure-history
          keep_reports: 20

      - name: Publish report to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: allure-history
```



### Разбор шагов: что делаем и зачем


| Строка  | Шаг                              | Что делает и зачем                                                                                                                                                                                                                                                     |
| ------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 378–382 | `on: push / pull_request`        | Запускает workflow при пуше или PR в **любую** ветку (`branches: [ "**" ]`) — тесты гоняются на каждое изменение                                                                                                                                                       |
| 384–385 | `permissions: contents: write`   | Даёт workflow права **на запись** в репозиторий — без этого шаг публикации отчёта на `gh-pages` (строка 430) не сможет запушить файлы                                                                                                                                  |
| 392–393 | `Checkout repository`            | Скачивает код репозитория на виртуальную машину GitHub Actions — без этого шага тестов и файлов проекта просто не будет                                                                                                                                                |
| 395–398 | `Set up Python 3.13`             | Устанавливает нужную версию Python на виртуальной машине (по умолчанию её там нет либо не той версии)                                                                                                                                                                  |
| 400–404 | `Install dependencies`           | Устанавливает `pytest`, `playwright`, `allure-pytest` и сами браузеры Playwright (`playwright install --with-deps chromium`) — без браузера Playwright не сможет открыть страницу                                                                                      |
| 406–409 | `Run UI tests`                   | Запускает тесты и пишет результаты в `allure-results/` (флаг `--alluredir`). `continue-on-error: true` — **ключевая строка**: если тесты упадут, workflow не остановится, и мы всё равно дойдём до шагов генерации/публикации отчёта (иначе упавший тест = нет отчёта) |
| 411–416 | `Load previous Allure history`   | Отдельным checkout скачивает **предыдущую** версию отчёта из ветки `gh-pages` (там уже лежит история прошлых прогонов). `continue-on-error: true` — на **первом** запуске ветки `gh-pages` ещё не существует, и это нормально                                          |
| 418–421 | `Copy history into results`      | Копирует папку `history/` из старого отчёта в свежие `allure-results/`, чтобы новый отчёт «увидел» историю прошлых прогонов (графики Trend/Retries). `2>/dev/null                                                                                                      |
| 423–428 | `Generate Allure report`         | Готовое действие (Action), которое запускает Allure CLI и собирает HTML-отчёт из `allure-results/` в папку `allure-history`. `keep_reports: 20` — хранить историю по последним 20 прогонам, не бесконечно                                                              |
| 430–435 | `Publish report to GitHub Pages` | Публикует папку `allure-history` (готовый HTML-отчёт) в отдельную ветку `gh-pages` — именно её потом отдаёт GitHub Pages как сайт                                                                                                                                      |


**Что важно один раз настроить руками в GitHub:**

1. `Settings → Pages` → Source: `gh-pages` branch (после первого запуска workflow)
2. `Settings → Actions → General → Workflow permissions` → **Read and write permissions**
  (иначе `peaceiris/actions-gh-pages` не сможет запушить отчёт)

После этого ссылка на отчёт будет доступна на:
`https://<user>.github.io/<repo>/`

---



## Доп. материал C — Интеграция в CI через Jenkins



### 1. Установить плагин в Jenkins

`Manage Jenkins → Plugins → Available` → найти **Allure Jenkins Plugin** → установить.

Затем: `Manage Jenkins → Tools → Allure Commandline installations` → добавить установку
(Jenkins сам скачает `allure` нужной версии — Java на агенте должна быть установлена).

### 2. `Jenkinsfile` (Declarative Pipeline) в корне репозитория

```groovy
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install pytest playwright pytest-playwright allure-pytest
                    playwright install --with-deps chromium
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest UI_project/test --alluredir=allure-results
                '''
            }
            post {
                always {
                    // Jenkins-плагин сам подхватывает историю по номерам билдов
                    allure includeProperties: false,
                           jdk: '',
                           results: [[path: 'allure-results']]
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
```

Ключевой момент: шаг `allure(...)` из Jenkinsfile — это специальный step,
который добавляет **History Trend** в Jenkins-версии Allure-отчёта автоматически,
подтягивая данные из **предыдущих билдов этого job** (ничего копировать вручную не нужно,
в отличие от GitHub Actions).

### 3. Настроить сам job в Jenkins

1. `New Item` → **Pipeline** (или **Multibranch Pipeline**, если несколько веток)
2. `Pipeline script from SCM` → указать репозиторий и путь к `Jenkinsfile`
3. После первого прогона на странице job появится пункт слева — **Allure Report**
4. Опционально: `Build Triggers → Poll SCM` или webhook из GitHub для авто-запуска

---



## Итоговая последовательность действий (чек-лист)

1. `pip install playwright pytest-playwright allure-pytest` + `playwright install`
2. `brew install allure` (+ Java 21, если нет)
3. Прогнать вручную: `pytest UI_project/test --alluredir=allure-results`
4. Посмотреть отчёт: `allure serve allure-results`
5. Создать `pytest.ini` с `addopts = --alluredir=allure-results --clean-alluredir`, чтобы дальше запускать просто `pytest`
6. Добавить `@allure.step` / `@allure.title` в тесты (по своему усмотрению)
7. Настроить перенос `history/` для локальной истории прогонов
8. Добавить `.github/workflows/tests.yml` + включить GitHub Pages на `gh-pages`
9. Или: установить Allure Jenkins Plugin + добавить `Jenkinsfile` с шагом `allure(...)`

