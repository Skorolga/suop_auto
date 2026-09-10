import pytest

from config.config import SUOP
from src.pages.auth_page import AuthPage


@pytest.mark.suop
def test_client_auth_smoke(browser):
    page = AuthPage(browser)
    browser.get(SUOP.MAIN_URL)
    page.auth_as_client()
    assert browser.current_url
