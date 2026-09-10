from datetime import datetime
import time
from selenium.webdriver.common.by import By
from src.pages.basic_page import BasicPage
from src.logger.formatted_logger import logger


class ClientPage(BasicPage):
    MENU_MAKE_ORDER = (By.XPATH, '//span[contains(text(), "Заказать услугу")]')
    BANNER_MAKE_ORDER = (By.XPATH, '//div/div/a[@href="/showcase/services/iaas"]')
    BUTTON_MAKE_ORDER = (By.XPATH, '//button[contains(text(), "Заказать")]')
    FORM_TITLE_CONF = (By.XPATH, '//h3[contains(text(), "Конфигурация")]')
    RADIOBUTTON_NEW_ORDER = (By.XPATH, '//div[contains(text(), "Создать новый заказ")]')
    DAY_COST = (By.XPATH, '//p[contains(text(), "В сутки без НДС")]/ancestor::div/div[@class="costs-icon"]/div[@class="costs-value"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[@type="submit"]')
    NEW_ORDER_NUM = (By.XPATH, '//p[contains(text(), "№")]')

    def make_order(self, timeout=180) -> str | bool:
        self.click(self.MENU_MAKE_ORDER)
        self.click(self.BANNER_MAKE_ORDER)
        self.click(self.BUTTON_MAKE_ORDER)
        self.wait_for_page_loaded(self.FORM_TITLE_CONF)
        self.click(self.RADIOBUTTON_NEW_ORDER)

        cost = self.check_cost(self.DAY_COST)
        assert cost, 'Стоимость заказа не рассчитана'

        self.click(self.SUBMIT_BUTTON)
        self.wait_for_page_loaded(self.NEW_ORDER_NUM, timeout)

        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout:
            elem = self.find_elem(self.NEW_ORDER_NUM, 2)
            if elem:
                order_num = ''.join(symbol for symbol in elem.text if symbol.isdigit())
                if order_num:
                    return order_num
            time.sleep(0.5)

        logger.error('Timeout при создании заказа')
        return False

    def check_cost(self, cost_locator, timeout=30) -> float | bool:
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout:
            elem = self.find_elem(cost_locator, 2)
            if elem:
                value = ''.join(ch for ch in elem.text if ch.isdigit() or ch == '.')
                if value and float(value) > 0:
                    return float(value)
            time.sleep(0.5)
        return False
