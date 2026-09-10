from datetime import datetime
from sys import platform
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import allure
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def browser():
    options = Options()
    prefs = {
        'profile.default_content_settings.popups': 0,
        'profile.managed_default_content_settings.notifications': 2,
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--disable-blink-features=BlockCredentialedSubresources')
    options.add_argument('--disable-web-resources-deprecation-warnings')

    if platform == 'linux':
        options.add_argument('--headless')

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    yield browser
    browser.quit()


@pytest.fixture
def pre_post_browser(browser):
    yield
    # Use configured/public-safe URL in real runs; no internal endpoint is stored here.


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        browser = None
        for fixture_name in item.fixturenames:
            if "browser" in fixture_name:
                browser = item.funcargs[fixture_name]
                break

        if browser and hasattr(browser, "get_screenshot_as_png"):
            screenshot = browser.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name='Скриншот ошибки',
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.hookimpl()
def pytest_sessionfinish(session):
    if not session.items:
        return
    dir_name = f'{session.items[0].name}_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}'
    cmd = f'allure generate -c ./allure-results --single-file -o ./allure-report/{dir_name}'
    proc = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, text=True)
    proc.wait()
