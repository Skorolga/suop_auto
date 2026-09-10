import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.config import SUOP
from src.logger.formatted_logger import logger
from src.pages.basic_page import BasicPage


class AuthPage(BasicPage):
    LOGIN_FORM = (By.ID, 'username')
    PASSWORD_FORM = (By.ID, 'password')
    SUBMIT_BTN = (By.XPATH, '//button[@type="submit"]')
    AUTH_MODAL_PAGINATION_NEXT = (By.XPATH, '//li[@class="pagination__next"]')
    AUTH_MODAL_MAIN_TABLE = (By.XPATH, '//table/tbody[contains(@class, "table-body")]')

    def auth_as_client(self):
        self.wait_for_page_loaded(self.LOGIN_FORM)
        self.type(self.LOGIN_FORM, SUOP.CLIENT_LOGIN)
        self.type(self.PASSWORD_FORM, SUOP.CLIENT_PASSWORD)
        self.click(self.SUBMIT_BTN)
        if SUOP.ORGANIZATION_CLIENT:
            self.select_role(SUOP.ORGANIZATION_CLIENT)

    def select_role(self, role: str) -> bool:
        locator = (By.XPATH, f"//div[contains(text(), '{role}')]")
        self.wait_for_page_loaded(self.AUTH_MODAL_MAIN_TABLE)
        try:
            self.click(locator, 2)
            return True
        except Exception:
            logger.info('Ищем роль на следующих страницах')

        try:
            next_page = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(self.AUTH_MODAL_PAGINATION_NEXT)
            )
        except Exception:
            return False

        while next_page:
            try:
                self.click(self.AUTH_MODAL_PAGINATION_NEXT, 1)
                self.click(locator, 1)
                return True
            except Exception:
                time.sleep(0.2)
                try:
                    next_page = WebDriverWait(self.browser, 2).until(
                        EC.presence_of_element_located(self.AUTH_MODAL_PAGINATION_NEXT)
                    )
                except Exception:
                    return False
        return False
