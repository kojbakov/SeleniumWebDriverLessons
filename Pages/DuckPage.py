from .BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


class DuckLocators:
    # Buttons
    ADD_TO_CART_LOCATOR = (By.NAME, "add_cart_product")
    # Other
    QUANTITY_LOCATOR = (By.CLASS_NAME, "quantity")


class Duck(BasePage):

    def add_duck_to_cart(self, duck_index: int):
        try:
            select_size = Select(self.driver.find_element_by_name("options[Size]"))
            select_size.select_by_value("Large")
        except NoSuchElementException:
            pass
        self.find_element(DuckLocators.ADD_TO_CART_LOCATOR).click()
        wait(self.driver, 10).until(EC.text_to_be_present_in_element(DuckLocators.QUANTITY_LOCATOR, str(duck_index)))
