import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from src.logger.formatted_logger import logger


class BasicPage:
    timeout = 60

    def __init__(self, browser):
        self.browser = browser

    def find_elem(self, locator: tuple[str, str], timeout=timeout) -> WebElement | bool:
        try:
            element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except (NoSuchElementException, TimeoutException):
            logger.warning(f'Элемент {locator[1]} не найден')
            return False

        try:
            WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            logger.warning(f'Элемент {locator[1]} не стал кликабельным за {timeout} секунд')
            return False

    def click(self, locator: tuple[str, str], timeout=timeout):
        element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except Exception:
            self.browser.execute_script('arguments[0].click();', element)

    def wait_for_page_loaded(self, locator=None, timeout=timeout) -> bool:
        WebDriverWait(self.browser, timeout).until(
            lambda browser: browser.execute_script('return document.readyState') == 'complete'
        )
        if not locator:
            return True
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def type(self, locator, text):
        self.browser.find_element(*locator).send_keys(text)

    def get_text(self, locator):
        elem = self.find_elem(locator)
        return elem.text if elem else None

    def custom_clear(self, locator):
        elem = self.find_elem(locator)
        if elem:
            elem.click()
            elem.send_keys(Keys.BACKSPACE * 10)
            time.sleep(0.2)
