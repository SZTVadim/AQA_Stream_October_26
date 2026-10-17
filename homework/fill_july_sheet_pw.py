"""Актуализирует блок ДЗ на листе AQA July 2026 через Playwright."""

from pathlib import Path

from playwright.sync_api import sync_playwright

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1DS35CbTJtL39HmHpH-McnVoHsff3MBKzKyeDIeNnRQ4/edit"
    "?gid=1676918919#gid=1676918919"
)
PROFILE = Path(__file__).resolve().parents[1] / ".pw-profile"

# Строки 17–31: ДЗ 3–8, 10–18. Колонки B–K: Turukhanov … Agafonov
# Только смерженные PR от 28 сентября 2026.
UPDATES = {
    "I24": "❎",  # Kadyrova 11
    "K25": "❎",  # Agafonov 12
    "F26": "❎",  # Fedorov 13
    "F29": "❎",  # Fedorov 16
    "K29": "❎",  # Agafonov 16
    "F30": "❎",  # Fedorov 17
    "F31": "❎",  # Fedorov 18
}


def goto_cell(page, cell: str) -> None:
    box = page.locator("#t-name-box")
    box.click(click_count=3)
    box.fill(cell)
    page.keyboard.press("Enter")
    page.wait_for_timeout(350)
    page.keyboard.press("Escape")
    page.wait_for_timeout(150)


def type_into_cell(page, value: str) -> None:
    page.locator(".formula-bar").click()
    page.wait_for_timeout(200)
    page.keyboard.press("Meta+a")
    page.keyboard.type(value, delay=20)
    page.keyboard.press("Enter")
    page.wait_for_timeout(400)


def main() -> None:
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(PROFILE),
            channel="chrome",
            headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(SHEET_URL, wait_until="domcontentloaded")
        page.wait_for_selector("#t-name-box", timeout=120_000)
        page.wait_for_timeout(2500)
        for cell, value in UPDATES.items():
            print("set", cell, value)
            goto_cell(page, cell)
            type_into_cell(page, value)
        page.wait_for_timeout(5000)
        context.close()
        print("готово")


if __name__ == "__main__":
    main()
