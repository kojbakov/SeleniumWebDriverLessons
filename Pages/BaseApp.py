from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class BasePage:

    def __init__(self, driver, url="http://localhost/litecart/en/"):
        self.driver = driver
        self.base_url = url

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def go_to_site(self, url=None):
        return self.driver.get(self.base_url) if url is None else self.driver.get(url)

    def get_driver(self):
        return self.driver
