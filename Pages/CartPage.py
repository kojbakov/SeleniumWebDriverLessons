from .BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time


class CartLocators:
    # Buttons
    REMOVE_ITEM_LOCATOR = (By.NAME, "remove_cart_item")
    # Other
    SHORTCUT_LOCATOR = (By.CLASS_NAME, "shortcuts")


class Cart(BasePage):

    def remove_ducks_from_cart(self):
        remove_buttons = self.find_elements(CartLocators.REMOVE_ITEM_LOCATOR)
        find_not_empty_rows_xpath = "*//div[@id='order_confirmation-wrapper']/table/tbody/tr"
        empty_cart_xpath = "*//div[@id='checkout-cart-wrapper']/p/em[text()='There are no items in your cart.']"
        for i in range(len(remove_buttons)):
            order_table_rows = self.driver.find_elements_by_xpath(find_not_empty_rows_xpath)
            # если утка не последняя - жждем появление иконки для остановки карусели и кликаем
            if i != len(remove_buttons) - 1:
                time.sleep(1)
                self.find_element(CartLocators.SHORTCUT_LOCATOR).click()
            wait(self.driver, 5).until(
                EC.element_to_be_clickable(CartLocators.REMOVE_ITEM_LOCATOR)).click()
            time.sleep(1)
            if i == len(remove_buttons) - 1 and len(self.driver.find_elements_by_xpath(empty_cart_xpath)) == 1:
                pass
            else:
                wait(self.driver, 10).until(
                    lambda driver: len(self.driver.find_elements(By.XPATH, find_not_empty_rows_xpath)) ==
                    len(order_table_rows) - 1
                )
