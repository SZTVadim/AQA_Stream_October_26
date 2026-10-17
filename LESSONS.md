# Собираем UI-автотесты для OrangeHRM с нуля

Стек: Python + pytest + Playwright + Allure.
Тестируем демо-стенд: [https://opensource-demo.orangehrmlive.com](https://opensource-demo.orangehrmlive.com) (логин `Admin`, пароль `admin123`).

За два урока соберём проект целиком: от первого «грязного» теста до сквозного сценария
добавления сотрудника. Отчёты в Allure подключим в самом конце, когда весь проект будет готов.
Каждый шаг я объясняю, а код можно копировать как есть.

Финальная структура, к которой придём:

```
UI_project/
├── config/
│   ├── __init__.py
│   └── credentials.py
├── controls/
│   ├── __init__.py
│   ├── filter_control.py
│   ├── header_control.py
│   └── menu_control.py
├── enumeration/
│   ├── __init__.py
│   └── menu_tabs.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── auth_page.py
│   ├── personal_page.py
│   ├── dashboard_page.py
│   └── pim/
│       ├── __init__.py
│       ├── pim_page.py
│       ├── employee_list_page.py
│       ├── add_employee_page.py
│       └── personal_details_page.py
├── test/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_authorize.py
│   ├── test_dashboard.py
│   └── test_add_employee.py
├── utils/
│   ├── __init__.py
│   └── data_generator.py
├── .gitignore
├── pytest.ini
└── requirements.txt
```

Иерархия страниц, которую мы построим:

```
BasePage
├── AuthPage
└── PersonalPage  (+ MenuControl, HeaderControl)
    ├── DashboardPage
    └── PimPage
        ├── EmployeeListPage (+ FilterControl)
        ├── AddEmployeePage
        └── PersonalDetailsPage
```

---



# Урок 1. Фундамент и архитектура

К концу урока у нас будут зелёные тесты авторизации и дашборда, а главное — понятная
архитектура: страницы, контролы и фикстуры, на которые дальше ляжет любой новый тест.

## Шаг 1.1. Поднимаем окружение

Первым делом создаю папку проекта и виртуальное окружение. Без него у каждого будут
свои версии библиотек, и «у меня работает, у тебя нет» нам гарантировано.

```bash
mkdir UI_project && cd UI_project
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install pytest playwright
playwright install chromium
pip freeze > requirements.txt
```

`requirements.txt` нужен, чтобы любой из вас мог потом поднять проект одной командой:
`pip install -r requirements.txt`.

## Шаг 1.2. Пишем тест «как не надо»

Сначала покажу, как выглядит тест без архитектуры. Создаю папку `test`, а в ней файл `test/test_dirty.py`:

```python
from playwright.sync_api import sync_playwright, expect


def test_login_dirty():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.fill("[name=username]", "Admin")
        page.fill("[name=password]", "admin123")
        page.click("[type=submit]")
        expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
        browser.close()
```

Запускаю:

```bash
pytest test/test_dirty.py -v
```

Тест работает. Но посмотрите, что тут лежит в одной куче: запуск браузера, URL стенда,
селекторы, данные для входа и проверка. Представьте, что таких тестов 50, и разработчик
поменял `name=username` на `id=login`. Нам придётся править 50 файлов.

Дальше мы разнесём всё это по своим местам. Этот файл скоро удалим.

## Шаг 1.3. Выносим браузер в фикстуры

Открыть и закрыть браузер — это не логика теста, а подготовка. В pytest для этого
есть фикстуры. Создаю `test/conftest.py`: pytest сам находит этот файл и даёт
фикстуры всем тестам рядом.

```python
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    # browser = playwright_instance.chromium.launch(headless=False, slow_mo=1000)  # чтобы видеть шаги
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context()
    try:
        yield context
    finally:
        context.close()


se
```

Здесь важно понять несколько вещей:

- `yield`: всё, что до него, выполняется перед тестом, всё, что после, — после теста.
Так мы гарантируем, что браузер закроется.
- `scope="session"`: Playwright запускается один раз на весь прогон, а браузер — на каждый тест.
- `context` — это как отдельный профиль браузера: свои cookies, свой localStorage.
Каждый тест получает чистое состояние.
- Фикстуры цепляются друг за друга: `page` просит `context`, `context` просит `browser`.
Pytest сам выстраивает этот порядок.



## Шаг 1.4. BasePage — базовый класс всех страниц

Теперь сам Page Object. Идея простая: каждая страница сайта — это класс. В нём лежат
селекторы этой страницы и действия, которые на ней можно сделать.

Создаю папку `pages`, а в ней пустой файл `__init__.py`. Этот файл превращает папку
в пакет Python, и тогда из других мест можно писать `from pages.base_page import BasePage`.
Дальше для каждой новой папки с кодом я буду делать то же самое.

Начинаю с базового класса: в нём будет то, что нужно абсолютно каждой странице.
Файл `pages/base_page.py`:

```python
from playwright.sync_api import Page


class BasePage:
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php"

    def __init__(self, page: Page):
        self.page = page

    def full_url(self, url, id_user=None):
        if id_user:
            return f"{self.BASE_URL}/{url}/{id_user}"
        else:
            return f"{self.BASE_URL}/{url}"

    def open_page(self, url, id_user=None):
        self.page.goto(self.full_url(url, id_user))

    def element(self, selector):
        return self.page.locator(selector)
```

`BASE_URL` лежит в одном месте. Если завтра нам дадут другой стенд, мы поменяем одну строку.

## Шаг 1.5. AuthPage — страница логина

Каждую страницу я буду строить по одному и тому же шаблону из четырёх блоков:

1. **Селекторы** — строки, по которым ищем элементы.
2. **Локаторы** — методы, которые возвращают объект элемента.
3. **Методы** — атомарные действия: ввести, нажать.
4. **Комбинированные методы** — сценарии из нескольких действий.

Файл `pages/auth_page.py`:

```python
from pages.base_page import BasePage


class AuthPage(BasePage):
    PAGE_URL = "auth/login"

    # селекторы
    _header_selector = ".orangehrm-login-title"
    _username_selector = "[name=username]"
    _password_selector = "[name=password]"
    _submit_selector = "[type=submit]"
    _forgot_password_selector = ".orangehrm-login-forgot-header"
    _copyright_wrapper_selector = ".orangehrm-copyright-wrapper"

    # локаторы
    def header_locator(self):
        return self.element(self._header_selector)

    def username_locator(self):
        return self.element(self._username_selector)

    def password_locator(self):
        return self.element(self._password_selector)

    def submit_locator(self):
        return self.element(self._submit_selector)

    def forgot_password_locator(self):
        return self.element(self._forgot_password_selector)

    def copyright_wrapper_locator(self):
        return self.element(self._copyright_wrapper_selector)

    # методы
    def fill_username(self, username):
        self.username_locator().fill(username)

    def fill_password(self, password):
        self.password_locator().fill(password)

    def click_login(self):
        self.submit_locator().click()

    # комбинированные методы
    def authorize(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()
```

Обратите внимание: селекторы начинаются с `_`. Это договорённость о том, что тест не должен
трогать их напрямую, а работает только через локаторы и методы.

## Шаг 1.6. Выносим данные для входа

Логин и пароль не пишем в тесте. Создаю папку `config` с пустым `__init__.py`
и файл `config/credentials.py`:

```python
USERNAME = "Admin"
PASSWORD = "admin123"
```

В реальных проектах пароли не коммитят в репозиторий, а берут из переменных окружения.
Нам для демо-стенда так достаточно.

## Шаг 1.7. Фикстура страницы логина

Теперь `conftest.py` начнёт импортировать код из `pages` и `config`. Чтобы pytest
нашёл эти пакеты, добавляю пустой `__init__.py` и в папку `test`. Тогда pytest считает
корнем проекта `UI_project`, и импорты `from pages...` работают. Без этого файла будет
ошибка `ModuleNotFoundError: No module named 'pages'`.

Добавляю в `test/conftest.py` импорт наверх и фикстуру вниз:

```python
from pages.auth_page import AuthPage
```

```python
@pytest.fixture
def auth_page(page) -> AuthPage:
    auth_page = AuthPage(page)
    auth_page.open_page(auth_page.PAGE_URL)
    return auth_page
```

Теперь любой тест, которому нужна открытая страница логина, просто пишет `auth_page` в аргументах.

## Шаг 1.8. Первый нормальный тест

Файл `test/test_authorize.py`:

```python
from playwright.sync_api import expect

from config.credentials import USERNAME, PASSWORD


class TestAuthorize:
    def test_authorize(self, auth_page):
        auth_page.authorize(USERNAME, PASSWORD)
        expect(auth_page.page).to_have_url(auth_page.full_url("dashboard/index"))

    def test_visible_elements(self, auth_page):
        expect(auth_page.submit_locator()).to_be_visible()
        expect(auth_page.username_locator()).to_be_visible()
        expect(auth_page.header_locator()).to_be_visible()
        expect(auth_page.password_locator()).to_be_visible()
        expect(auth_page.copyright_wrapper_locator()).to_be_visible()
```

Запускаю из корня проекта:

```bash
pytest test/test_authorize.py -v
```

Сравните с грязным тестом: теперь тест читается как сценарий. Ни одного селектора
и ни одного URL в нём нет. Если поменяется селектор, я правлю его в одном месте, в `AuthPage`.

Про `expect`: это проверка Playwright с автоожиданием. Она сама ждёт до 5 секунд,
пока элемент появится или URL сменится. Поэтому никаких `time.sleep` мы не пишем.

Грязный тест больше не нужен:

```bash
rm test/test_dirty.py
```



## Шаг 1.9. Константы меню

Дальше мы идём внутрь приложения, где есть боковое меню. Чтобы не писать в коде строки
вроде `"PIM"` в разных местах, заводим перечисление. Создаю папку `enumeration`
с пустым `__init__.py` и файл `enumeration/menu_tabs.py`:

```python
class MenuTabs:
    ADMIN = "Admin"
    PIM = "PIM"
    DASHBOARD = "Dashboard"
```



## Шаг 1.10. Контролы: хедер

Залогиньтесь на сайте и посмотрите: левое меню и верхний хедер одинаковые на каждой
странице. Если описать их в каждом Page Object, мы получим копипасту.

Поэтому выносим их в отдельные классы — контролы. Контрол — это кусок интерфейса,
который живёт на многих страницах. Страница не наследуется от него, а содержит его
внутри себя («у страницы есть меню»).

Создаю папку `controls` с пустым `__init__.py` и файл `controls/header_control.py`:

```python
from playwright.sync_api import Page


class HeaderControl:
    def __init__(self, page: Page):
        self.page = page

    # селекторы
    _header_selector = ".oxd-topbar-header-breadcrumb-module"
    _upgrade_button_selector = ".orangehrm-upgrade-button"
    _user_menu_selector = ".oxd-userdropdown-tab"
    _about_from_menu_selector = "//*[text()='About']"
    _support_from_menu_selector = "//*[text()='Support']"
    _change_password_from_menu_selector = "//*[text()='Change Password']"
    _logout_from_menu_selector = "//*[text()='Logout']"
    _help_button_selector = "//*[@title='Help']"

    # локаторы
    def header_locator(self):
        return self.page.locator(self._header_selector)

    def upgrade_button_locator(self):
        return self.page.locator(self._upgrade_button_selector)

    def user_menu_locator(self):
        return self.page.locator(self._user_menu_selector)

    def about_from_menu_locator(self):
        return self.page.locator(self._about_from_menu_selector)

    def support_from_menu_locator(self):
        return self.page.locator(self._support_from_menu_selector)

    def change_password_from_menu_locator(self):
        return self.page.locator(self._change_password_from_menu_selector)

    def logout_from_menu_locator(self):
        return self.page.locator(self._logout_from_menu_selector)

    def help_button_locator(self):
        return self.page.locator(self._help_button_selector)
```



## Шаг 1.11. Контролы: боковое меню

Файл `controls/menu_control.py`:

```python
from playwright.sync_api import Page

from enumeration.menu_tabs import MenuTabs


class MenuControl:
    def __init__(self, page: Page):
        self.page = page

    # селекторы
    _logo_selector = "[alt='client brand banner']"
    _search_input_selector = "//input[@placeholder='Search']"
    _admin_selector = "//*[text()='Admin']"
    _pim_selector = "//*[text()='PIM']"
    _leave_selector = "//*[text()='Leave']"
    _time_selector = "//*[text()='Time']"
    _dashboard_selector = "//*[text()='Dashboard']"
    _recruitment_selector = "//*[text()='Recruitment']"
    _my_info_selector = "//*[text()='My Info']"
    _performance_selector = "//*[text()='Performance']"
    _directory_selector = "//*[text()='Directory']"
    _maintenance_selector = "//*[text()='Maintenance']"
    _claim_selector = "//*[text()='Claim']"
    _buzz_selector = "//*[text()='Buzz']"
    _collapse_menu_selector = ".oxd-icon-button.oxd-main-menu-button"

    # локаторы
    def logo_locator(self):
        return self.page.locator(self._logo_selector)

    def search_input_locator(self):
        return self.page.locator(self._search_input_selector)

    def admin_locator(self):
        return self.page.locator(self._admin_selector)

    def pim_locator(self):
        return self.page.locator(self._pim_selector)

    def leave_locator(self):
        return self.page.locator(self._leave_selector)

    def time_locator(self):
        return self.page.locator(self._time_selector)

    def dashboard_locator(self):
        return self.page.locator(self._dashboard_selector)

    def recruitment_locator(self):
        return self.page.locator(self._recruitment_selector)

    def my_info_locator(self):
        return self.page.locator(self._my_info_selector)

    def performance_locator(self):
        return self.page.locator(self._performance_selector)

    def directory_locator(self):
        return self.page.locator(self._directory_selector)

    def maintenance_locator(self):
        return self.page.locator(self._maintenance_selector)

    def claim_locator(self):
        return self.page.locator(self._claim_selector)

    def buzz_locator(self):
        return self.page.locator(self._buzz_selector)

    def collapse_menu_locator(self):
        return self.page.locator(self._collapse_menu_selector)

    # методы
    def switch_to_tab(self, menu_section):
        menu_map = {
            MenuTabs.PIM: self.pim_locator(),
            MenuTabs.ADMIN: self.admin_locator(),
            MenuTabs.DASHBOARD: self.dashboard_locator(),
        }
        menu_map[menu_section].click()

    def open_dashboard(self):
        self.switch_to_tab(MenuTabs.DASHBOARD)

    def open_admin(self):
        self.switch_to_tab(MenuTabs.ADMIN)

    def open_pim(self):
        self.switch_to_tab(MenuTabs.PIM)
```

Посмотрите на `switch_to_tab`: словарь сопоставляет вкладку с её локатором. Один метод
обслуживает сколько угодно пунктов меню, а `open_pim()` и другие — это короткие
удобные обёртки для тестов.

Обратите внимание на `_collapse_menu_selector`: два класса одного элемента в CSS
пишутся слитно через точку, `.class1.class2`. Если поставить пробел, это будет поиск
`class2` внутри `class1`, и элемент не найдётся.

## Шаг 1.12. PersonalPage — страница залогиненного пользователя

Теперь нужен промежуточный слой: «любая страница после логина». Он наследуется от
`BasePage` и сразу подключает меню и хедер. Все следующие страницы будут наследоваться
от него и получат меню автоматически.

Файл `pages/personal_page.py`:

```python
from controls.header_control import HeaderControl
from controls.menu_control import MenuControl
from pages.base_page import BasePage


class PersonalPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.menu_control = MenuControl(self.page)
        self.header_control = HeaderControl(self.page)
```

`super().__init__(page)` вызывает конструктор `BasePage`, чтобы у нас появился `self.page`.
Без этого вызова контролам нечего было бы передать.

## Шаг 1.13. DashboardPage

Файл `pages/dashboard_page.py`:

```python
from pages.personal_page import PersonalPage


class DashboardPage(PersonalPage):
    PAGE_URL = "dashboard/index"

    # селекторы
    _time_at_work_selector = "//*[contains(@class,'bi-clock-fill')]/../../../.."
    _my_actions_selector = "//*[contains(@class,'bi-list-check')]/../../../.."
    _quick_launch_selector = "//*[contains(@class,'bi-lightning-charge-fill')]/../../../.."
    _buzz_latest_posts_selector = "//*[contains(@class,'bi-camera-fill')]/../../../.."

    # локаторы
    def time_at_work_locator(self):
        return self.element(self._time_at_work_selector)

    def my_actions_locator(self):
        return self.element(self._my_actions_selector)

    def quick_launch_locator(self):
        return self.element(self._quick_launch_selector)

    def buzz_latest_posts_locator(self):
        return self.element(self._buzz_latest_posts_selector)
```

Про эти XPath: у виджетов нет нормальных уникальных атрибутов, поэтому я нахожу иконку
и поднимаюсь от неё к карточке через `/..`. Это рабочий, но хрупкий приём: если
вложенность поменяется, селектор сломается. В реальном проекте в такой ситуации
просят разработчиков добавить `data-testid`.

## Шаг 1.14. Фикстура «уже залогинен»

Тесту дашборда не нужно каждый раз заново описывать логин, это его предусловие.
Делаю фикстуру, которая логинится сама и отдаёт готовую страницу.

Добавляю в `test/conftest.py` импорты наверх:

```python
from config.credentials import USERNAME, PASSWORD
from pages.dashboard_page import DashboardPage
```

и фикстуры вниз:

```python
@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    return DashboardPage(page)


@pytest.fixture
def dashboard(auth_page: AuthPage, dashboard_page: DashboardPage) -> DashboardPage:
    auth_page.authorize(USERNAME, PASSWORD)
    return dashboard_page
```

Разница между ними:

- `dashboard_page` — просто объект страницы, ничего не делает.
- `dashboard` — открыл логин, залогинился и вернул дашборд. Это основная точка входа
для всех тестов, где нужен авторизованный пользователь.

Обе фикстуры получают один и тот же `page`, потому что pytest в рамках одного теста
создаёт фикстуру один раз. Поэтому `auth_page` и `dashboard_page` работают с одной вкладкой.

## Шаг 1.15. Обновляем тест авторизации и пишем тест дашборда

Переписываю `test/test_authorize.py`: теперь URL дашборда берём из самой страницы
и дополнительно проверяем хедер через контрол.

```python
from playwright.sync_api import expect

from config.credentials import USERNAME, PASSWORD


class TestAuthorize:
    def test_authorize(self, auth_page, dashboard_page):
        auth_page.authorize(USERNAME, PASSWORD)
        expect(dashboard_page.page).to_have_url(dashboard_page.full_url(dashboard_page.PAGE_URL))
        expect(dashboard_page.header_control.header_locator()).to_have_text("Dashboard")

    def test_visible_elements(self, auth_page):
        expect(auth_page.submit_locator()).to_be_visible()
        expect(auth_page.username_locator()).to_be_visible()
        expect(auth_page.header_locator()).to_be_visible()
        expect(auth_page.password_locator()).to_be_visible()
        expect(auth_page.copyright_wrapper_locator()).to_be_visible()
```

Файл `test/test_dashboard.py`:

```python
from playwright.sync_api import expect


class TestDashboard:
    def test_visible_elements(self, dashboard):
        expect(dashboard.buzz_latest_posts_locator()).to_be_visible()
        expect(dashboard.my_actions_locator()).to_be_visible()
        expect(dashboard.time_at_work_locator()).to_be_visible()
        expect(dashboard.quick_launch_locator()).to_be_visible()
```

Смотрите, насколько короткий тест: залогиниться — одно слово `dashboard` в аргументах.

```bash
pytest -v
```



## Домашнее задание к уроку 2

1. Написать негативный тест: неверный пароль → видно сообщение `Invalid credentials`
  (добавить селектор и локатор ошибки в `AuthPage`).
2. Дописать в `switch_to_tab` оставшиеся вкладки (Leave, Time, My Info, Directory...)
  и методы `open_...` для них.
3. Добавить в `HeaderControl` метод `logout()`: открыть меню пользователя, нажать Logout.
  Написать тест: после логаута URL снова `auth/login`.

---



# Урок 2. Бизнес-сценарий, доводка проекта и Allure

Сегодня собираем настоящий e2e-сценарий через несколько страниц: логин → PIM →
Add Employee → сохранение → проверка карточки сотрудника. Потом приводим проект
в порядок и в самом конце подключаем отчёты Allure.

## Шаг 2.1. PimPage — общая страница модуля PIM

У модуля PIM есть верхние вкладки: Employee List, Add Employee, Reports, Configuration.
Они одинаковые на всех страницах PIM. Поэтому делаю ещё один уровень наследования:
`PimPage` описывает навигацию модуля, а конкретные страницы PIM наследуются от неё.

Страниц PIM будет несколько, поэтому складываю их в отдельную папку. Создаю внутри
`pages` папку `pim` с пустым `__init__.py` и файл `pages/pim/pim_page.py`:

```python
from pages.personal_page import PersonalPage


class PimPage(PersonalPage):
    PAGE_URL = "pim/viewEmployeeList"

    # селекторы
    _employee_list_selector = "//*[text()='Employee List']"
    _add_employee_selector = "//*[text()='Add Employee']"
    _reports_selector = "//*[text()='Reports']"
    _configuration_selector = "//*[text()='Configuration ']"
    _optional_fields_selector = "//*[text()='Optional Fields']"
    _custom_fields_selector = "//*[text()='Custom Fields']"
    _data_import_selector = "//*[text()='Data Import']"
    _reporting_methods_selector = "//*[text()='Reporting Methods']"
    _termination_reasons_selector = "//*[text()='Termination Reasons']"

    # локаторы
    def employee_list_locator(self):
        return self.element(self._employee_list_selector)

    def add_employee_locator(self):
        return self.element(self._add_employee_selector)

    def reports_locator(self):
        return self.element(self._reports_selector)

    def configuration_locator(self):
        return self.element(self._configuration_selector)

    def optional_fields_locator(self):
        return self.element(self._optional_fields_selector)

    def custom_fields_locator(self):
        return self.element(self._custom_fields_selector)

    def data_import_locator(self):
        return self.element(self._data_import_selector)

    def reporting_methods_locator(self):
        return self.element(self._reporting_methods_selector)

    def termination_reasons_locator(self):
        return self.element(self._termination_reasons_selector)

    # методы
    def open_add_employee(self):
        self.add_employee_locator().click()
```

Обратите внимание на пробел в `'Configuration '`: на сайте в тексте этой вкладки
действительно есть пробел в конце. `text()=` сравнивает строку точно, поэтому без
пробела элемент не найдётся.

## Шаг 2.2. FilterControl — второй контрол

На списке сотрудников есть блок фильтров. Он встречается только на страницах со
списками, поэтому подключаю его не в `PersonalPage`, а только туда, где он нужен.

Файл `controls/filter_control.py`:

```python
from playwright.sync_api import Page


class FilterControl:
    def __init__(self, page: Page):
        self.page = page

    # селекторы
    _employee_information_selector = ".oxd-table-filter-title"
    _reset_button_selector = ".oxd-button--ghost"
    _search_button_selector = ".orangehrm-left-space"

    # локаторы
    def employee_information_locator(self):
        return self.page.locator(self._employee_information_selector)

    def reset_button_locator(self):
        return self.page.locator(self._reset_button_selector)

    def search_button_locator(self):
        return self.page.locator(self._search_button_selector)
```



## Шаг 2.3. EmployeeListPage

Файл `pages/pim/employee_list_page.py`:

```python
from controls.filter_control import FilterControl
from pages.pim.pim_page import PimPage


class EmployeeListPage(PimPage):
    PAGE_URL = "pim/viewEmployeeList"

    def __init__(self, page):
        super().__init__(page)
        self.filter_control = FilterControl(self.page)

    # селекторы
    _add_button_selector = "//*[contains(@class,'bi-plus')]/.."

    # локаторы
    def add_button_locator(self):
        return self.element(self._add_button_selector)

    # методы
    def click_add_button(self):
        self.add_button_locator().click()
```

Сравните с `PersonalPage`: там мы так же через `super().__init__` расширяли конструктор
и добавляли контролы. Здесь та же идея: страница получила меню и хедер от родителя
и добавила фильтр.

## Шаг 2.4. Генератор тестовых данных

Прежде чем писать форму, думаем о данных. У сотрудника есть поле Employee Id, и оно
должно быть уникальным. Если захардкодить `"12345"`, тест пройдёт один раз, а на втором
запуске упадёт с ошибкой «Employee Id already exists».

Поэтому выношу генерацию данных в отдельный слой. Создаю папку `utils` с пустым
`__init__.py` и файл `utils/data_generator.py`:

```python
import random
from dataclasses import dataclass


@dataclass
class Employee:
    first_name: str
    middle_name: str
    last_name: str
    employee_id: str


def generate_employee() -> Employee:
    suffix = random.randint(1000, 9999)
    return Employee(
        first_name=f"first_{suffix}",
        middle_name=f"middle_{suffix}",
        last_name=f"last_{suffix}",
        employee_id=str(random.randint(1000000, 9999999)),
    )
```

`dataclass` — это класс, у которого Python сам генерирует конструктор по полям.
Удобно передавать одного «сотрудника» целиком, а не четыре отдельных строки.

## Шаг 2.5. AddEmployeePage

Файл `pages/pim/add_employee_page.py`:

```python
from pages.pim.pim_page import PimPage
from utils.data_generator import Employee


class AddEmployeePage(PimPage):
    PAGE_URL = "pim/addEmployee"

    # селекторы
    _add_employee_title_selector = ".orangehrm-main-title"
    _input_first_name_selector = "[name='firstName']"
    _input_middle_name_selector = "[name='middleName']"
    _input_last_name_selector = "[name='lastName']"
    _employee_id_selector = "//*[contains(@class,'oxd-grid-2')]//input"
    _cancel_button_selector = ".oxd-button--ghost"
    _save_button_selector = ".orangehrm-left-space"

    # локаторы
    def add_employee_title_locator(self):
        return self.element(self._add_employee_title_selector)

    def input_first_name_locator(self):
        return self.element(self._input_first_name_selector)

    def input_middle_name_locator(self):
        return self.element(self._input_middle_name_selector)

    def input_last_name_locator(self):
        return self.element(self._input_last_name_selector)

    def employee_id_locator(self):
        return self.element(self._employee_id_selector)

    def cancel_button_locator(self):
        return self.element(self._cancel_button_selector)

    def save_button_locator(self):
        return self.element(self._save_button_selector)

    # методы
    def fill_first_name(self, first_name):
        self.input_first_name_locator().fill(first_name)

    def fill_middle_name(self, middle_name):
        self.input_middle_name_locator().fill(middle_name)

    def fill_last_name(self, last_name):
        self.input_last_name_locator().fill(last_name)

    def fill_employee_id(self, employee_id):
        self.employee_id_locator().fill(employee_id)

    def click_save_button(self):
        self.save_button_locator().click()

    def click_cancel_button(self):
        self.cancel_button_locator().click()

    # комбинированные методы
    def add_employee(self, employee: Employee):
        self.fill_first_name(employee.first_name)
        self.fill_middle_name(employee.middle_name)
        self.fill_last_name(employee.last_name)
        self.fill_employee_id(employee.employee_id)
        self.click_save_button()
```

Здесь хорошо видна разница двух видов методов:

- Атомарные (`fill_first_name`) дают гибкость. Например, для негативного теста
«сохранить без фамилии» я просто не вызову `fill_last_name`.
- Комбинированный (`add_employee`) делает тест коротким, когда нужен обычный сценарий.

`fill()` сначала очищает поле. Это важно для Employee Id: сайт подставляет туда
своё значение, а мы его перезаписываем.

## Шаг 2.6. PersonalDetailsPage

После сохранения нас перекидывает на карточку сотрудника. Файл `pages/pim/personal_details_page.py`:

```python
from pages.pim.pim_page import PimPage


class PersonalDetailsPage(PimPage):
    PAGE_URL = "pim/viewPersonalDetails/empNumber"

    # селекторы
    _title_selector = "//h6[text()='Personal Details']"

    # локаторы
    def title_locator(self):
        return self.element(self._title_selector)
```

URL этой страницы заканчивается номером сотрудника, например `.../empNumber/123`.
Мы заранее не знаем этот номер, поэтому в тесте будем проверять URL по регулярке.
А если номер известен, у нас уже есть `full_url(PAGE_URL, id_user)` из `BasePage`.

## Шаг 2.7. Фикстуры для PIM

Добавляю в `test/conftest.py` импорты:

```python
from pages.pim.add_employee_page import AddEmployeePage
from pages.pim.employee_list_page import EmployeeListPage
from pages.pim.personal_details_page import PersonalDetailsPage
```

и фикстуры:

```python
@pytest.fixture
def employee_list_page(page) -> EmployeeListPage:
    return EmployeeListPage(page)


@pytest.fixture
def add_employee_page(page) -> AddEmployeePage:
    return AddEmployeePage(page)


@pytest.fixture
def personal_details_page(page) -> PersonalDetailsPage:
    return PersonalDetailsPage(page)
```



## Шаг 2.8. Тест добавления сотрудника

Файл `test/test_add_employee.py`:

```python
import re

from playwright.sync_api import expect

from utils.data_generator import generate_employee


class TestAddEmployee:
    def test_add_employee(self, dashboard, employee_list_page, add_employee_page, personal_details_page):
        employee = generate_employee()

        dashboard.menu_control.open_pim()
        employee_list_page.open_add_employee()
        add_employee_page.add_employee(employee)

        expect(personal_details_page.title_locator()).to_be_visible()
        expect(personal_details_page.page).to_have_url(re.compile(personal_details_page.PAGE_URL))
```

Прочитайте этот тест вслух — он читается как тест-кейс из TMS: «залогинились, открыли PIM,
открыли добавление, добавили сотрудника, проверили, что открылась его карточка».
Именно ради этого мы строили всю архитектуру.

```bash
pytest test/test_add_employee.py -v
```



## Шаг 2.9. Маркеры

Когда тестов сотни, хочется быстро прогнать только самые важные. Для этого есть маркеры.
Создаю в корне проекта `pytest.ini`:

```ini
[pytest]
markers =
    smoke: быстрые критичные проверки
```

Помечаю тест авторизации в `test/test_authorize.py`:

```python
import pytest
from playwright.sync_api import expect

from config.credentials import USERNAME, PASSWORD


class TestAuthorize:
    @pytest.mark.smoke
    def test_authorize(self, auth_page, dashboard_page):
        auth_page.authorize(USERNAME, PASSWORD)
        expect(dashboard_page.page).to_have_url(dashboard_page.full_url(dashboard_page.PAGE_URL))
        expect(dashboard_page.header_control.header_locator()).to_have_text("Dashboard")

    def test_visible_elements(self, auth_page):
        expect(auth_page.submit_locator()).to_be_visible()
        expect(auth_page.username_locator()).to_be_visible()
        expect(auth_page.header_locator()).to_be_visible()
        expect(auth_page.password_locator()).to_be_visible()
        expect(auth_page.copyright_wrapper_locator()).to_be_visible()
```

Запуск только smoke:

```bash
pytest -m smoke -v
```



## Шаг 2.10. .gitignore

В репозиторий не должны попадать виртуальное окружение, кэш и настройки IDE.
Файл `.gitignore` в корне проекта:

```
.venv/
__pycache__/
.pytest_cache/
.idea/
.vscode/
```

Прогоняю всё целиком и убеждаюсь, что проект зелёный:

```bash
pytest -v
```

Всё, проект готов. Теперь, когда тестов и страниц достаточно, подключаем отчёты.

---



## Шаг 2.11. Подключаем Allure

По выводу консоли сложно понять, на каком шаге упал тест и как выглядела страница
в этот момент. Allure строит HTML-отчёт с шагами, временем и вложениями.

Я специально подключаю его в самом конце: так видно, что отчётность — это отдельный
слой поверх готового проекта. Архитектуру мы не трогаем, только добавляем разметку.

### Установка

Ставлю библиотеку в проект и консольную утилиту на компьютер (утилиту один раз):

```bash
pip install allure-pytest
pip freeze > requirements.txt

brew install allure        # macOS
# Windows: scoop install allure
```



### Настройка pytest.ini

Чтобы не писать флаги руками при каждом запуске, добавляю их в `pytest.ini`:

```ini
[pytest]
addopts = --alluredir=allure-results --clean-alluredir
markers =
    smoke: быстрые критичные проверки
```

И добавляю результаты Allure в `.gitignore`:

```
.venv/
__pycache__/
.pytest_cache/
.idea/
.vscode/
allure-results/
allure-report/
```



### Первый отчёт без разметки

Сначала просто запускаю тесты и открываю отчёт, ничего не размечая:

```bash
pytest
allure serve allure-results
```

Отчёт есть, но в нём только названия функций и никаких шагов. Разметим их.

Важно: запускаем всегда из корня `UI_project`. Если запустить из папки `test/`,
папка `allure-results` создастся внутри неё, и отчёт окажется не там, где вы его ищете.

### Шаги в Page Object

Главное правило: декораторы шагов ставлю в Page Object, а не в тестах. Тогда каждый
вызов метода сам появится в отчёте как шаг, и тесты переписывать не нужно.

`pages/base_page.py` целиком:

```python
import allure

from playwright.sync_api import Page


class BasePage:
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php"

    def __init__(self, page: Page):
        self.page = page

    def full_url(self, url, id_user=None):
        if id_user:
            return f"{self.BASE_URL}/{url}/{id_user}"
        else:
            return f"{self.BASE_URL}/{url}"

    @allure.step("Открываем страницу")
    def open_page(self, url, id_user=None):
        self.page.goto(self.full_url(url, id_user))

    def element(self, selector):
        return self.page.locator(selector)
```

В `pages/auth_page.py` добавляю `import allure` в самый верх и заменяю блоки методов:

```python
    # методы
    @allure.step("Ввод Username")
    def fill_username(self, username):
        self.username_locator().fill(username)

    @allure.step("Ввод Password")
    def fill_password(self, password):
        self.password_locator().fill(password)

    @allure.step("Нажать кнопку Login")
    def click_login(self):
        self.submit_locator().click()

    # комбинированные методы
    @allure.step("Авторизоваться")
    def authorize(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()
```

В `controls/menu_control.py` добавляю `import allure` в самый верх и шаг на переход по меню:

```python
    @allure.step("Переход в раздел меню")
    def switch_to_tab(self, menu_section):
        menu_map = {
            MenuTabs.PIM: self.pim_locator(),
            MenuTabs.ADMIN: self.admin_locator(),
            MenuTabs.DASHBOARD: self.dashboard_locator(),
        }
        menu_map[menu_section].click()
```

В `pages/pim/pim_page.py` добавляю `import allure` в самый верх и заменяю блок методов:

```python
    # методы
    @allure.step("Открыть вкладку Add Employee")
    def open_add_employee(self):
        self.add_employee_locator().click()
```

В `pages/pim/employee_list_page.py` добавляю `import allure` в самый верх и заменяю блок методов:

```python
    # методы
    @allure.step("Нажать кнопку Add")
    def click_add_button(self):
        self.add_button_locator().click()
```

В `pages/pim/add_employee_page.py` добавляю `import allure` в самый верх и заменяю блоки методов:

```python
    # методы
    @allure.step("Ввод First Name")
    def fill_first_name(self, first_name):
        self.input_first_name_locator().fill(first_name)

    @allure.step("Ввод Middle Name")
    def fill_middle_name(self, middle_name):
        self.input_middle_name_locator().fill(middle_name)

    @allure.step("Ввод Last Name")
    def fill_last_name(self, last_name):
        self.input_last_name_locator().fill(last_name)

    @allure.step("Ввод Employee Id")
    def fill_employee_id(self, employee_id):
        self.employee_id_locator().fill(employee_id)

    @allure.step("Нажать кнопку Save")
    def click_save_button(self):
        self.save_button_locator().click()

    @allure.step("Нажать кнопку Cancel")
    def click_cancel_button(self):
        self.cancel_button_locator().click()

    # комбинированные методы
    @allure.step("Заполнить форму и сохранить сотрудника")
    def add_employee(self, employee: Employee):
        self.fill_first_name(employee.first_name)
        self.fill_middle_name(employee.middle_name)
        self.fill_last_name(employee.last_name)
        self.fill_employee_id(employee.employee_id)
        self.click_save_button()
```

Шаги можно вкладывать: «Авторизоваться» в отчёте раскроется в «Ввод Username»,
«Ввод Password», «Нажать кнопку Login».

### Названия тестов

Тестам даю человеческие названия через `@allure.title`.

`test/test_authorize.py` целиком:

```python
import allure
import pytest
from playwright.sync_api import expect

from config.credentials import USERNAME, PASSWORD


class TestAuthorize:
    @pytest.mark.smoke
    @allure.title("Авторизация")
    def test_authorize(self, auth_page, dashboard_page):
        auth_page.authorize(USERNAME, PASSWORD)
        expect(dashboard_page.page).to_have_url(dashboard_page.full_url(dashboard_page.PAGE_URL))
        expect(dashboard_page.header_control.header_locator()).to_have_text("Dashboard")

    @allure.title("Проверка элементов на странице логина")
    def test_visible_elements(self, auth_page):
        expect(auth_page.submit_locator()).to_be_visible()
        expect(auth_page.username_locator()).to_be_visible()
        expect(auth_page.header_locator()).to_be_visible()
        expect(auth_page.password_locator()).to_be_visible()
        expect(auth_page.copyright_wrapper_locator()).to_be_visible()
```

`test/test_dashboard.py` целиком:

```python
import allure
from playwright.sync_api import expect


class TestDashboard:
    @allure.title("Проверка виджетов на дашборде")
    def test_visible_elements(self, dashboard):
        expect(dashboard.buzz_latest_posts_locator()).to_be_visible()
        expect(dashboard.my_actions_locator()).to_be_visible()
        expect(dashboard.time_at_work_locator()).to_be_visible()
        expect(dashboard.quick_launch_locator()).to_be_visible()
```

`test/test_add_employee.py` целиком:

```python
import re

import allure
from playwright.sync_api import expect

from utils.data_generator import generate_employee


class TestAddEmployee:
    @allure.title("Добавление сотрудника")
    def test_add_employee(self, dashboard, employee_list_page, add_employee_page, personal_details_page):
        employee = generate_employee()

        dashboard.menu_control.open_pim()
        employee_list_page.open_add_employee()
        add_employee_page.add_employee(employee)

        expect(personal_details_page.title_locator()).to_be_visible()
        expect(personal_details_page.page).to_have_url(re.compile(personal_details_page.PAGE_URL))
```



### Скриншот при падении

Когда тест упал, первое, что хочется увидеть, — как выглядела страница в этот момент.
Добавляю в `test/conftest.py` хук, который при падении прикладывает скриншот в Allure.

Импорт наверх:

```python
import allure
```

Хук вниз файла:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
```



### Смотрим итоговый отчёт

```bash
pytest
allure serve allure-results
```

Теперь внутри каждого теста видны шаги, а у тестов — нормальные названия.
Проверьте скриншот сами: сломайте любую проверку, например `to_have_text("Dashboard123")`,
снова запустите тесты и откройте отчёт. В упавшем тесте будет скриншот страницы.

---



## Итоговый [conftest.py](http://conftest.py)

Вот как должен выглядеть `test/conftest.py` целиком в конце курса. Сверьтесь со своим:

```python
import allure
import pytest
from playwright.sync_api import sync_playwright

from config.credentials import USERNAME, PASSWORD
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage
from pages.pim.add_employee_page import AddEmployeePage
from pages.pim.employee_list_page import EmployeeListPage
from pages.pim.personal_details_page import PersonalDetailsPage


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    # browser = playwright_instance.chromium.launch(headless=False, slow_mo=1000)  # чтобы видеть шаги
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    context = browser.new_context()
    try:
        yield context
    finally:
        context.close()


@pytest.fixture
def page(context):
    return context.new_page()


@pytest.fixture
def auth_page(page) -> AuthPage:
    auth_page = AuthPage(page)
    auth_page.open_page(auth_page.PAGE_URL)
    return auth_page


@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    return DashboardPage(page)


@pytest.fixture
def dashboard(auth_page: AuthPage, dashboard_page: DashboardPage) -> DashboardPage:
    auth_page.authorize(USERNAME, PASSWORD)
    return dashboard_page


@pytest.fixture
def employee_list_page(page) -> EmployeeListPage:
    return EmployeeListPage(page)


@pytest.fixture
def add_employee_page(page) -> AddEmployeePage:
    return AddEmployeePage(page)


@pytest.fixture
def personal_details_page(page) -> PersonalDetailsPage:
    return PersonalDetailsPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
```



## Финальное домашнее задание

1. Тест поиска сотрудника: создать сотрудника, перейти в Employee List, ввести его имя
  в фильтр (добавить в `FilterControl` поле Employee Name и метод `search_by_name`),
   нажать Search и проверить, что в таблице есть строка с его фамилией.
2. Негативный тест: сохранить сотрудника без Last Name → под полем видно `Required`.
3. Разметить шагами Allure все новые методы из домашних заданий.
4. Написать `README.md` с инструкцией: как установить зависимости, запустить тесты и открыть отчёт.

