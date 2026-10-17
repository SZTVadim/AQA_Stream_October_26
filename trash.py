from playwright.sync_api import Page, expect


def test_page(page: Page):
    page.goto("https://lahtajunior.ru/services/service-to-pediatr")

    expect(page.get_by_role("button", name="Записаться онлай", exact=True)).to_be_visible()