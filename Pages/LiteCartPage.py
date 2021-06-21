from .BaseApp import BasePage
from selenium.webdriver.common.by import By
from SysFunctions.sys_func import get_rgb
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time


class LiteCartLocators:
    REGULAR_PRICE_LOCATOR = (By.CLASS_NAME, 'regular-price')
    CAMPAIGNS_PRICE_LOCATOR = (By.CLASS_NAME, 'campaign-price')
    # inputs
    USERNAME_INPUT_LOCATOR = (By.NAME, "email")
    PASSWORD_INPUT_LOCATOR = (By.NAME, "password")
    # buttons
    LOGIN_BUTTON_LOCATOR = (By.NAME, "login")
    LOGOUT_BUTTON_LOCATOR = (By.XPATH, "//*[@id='box-account']/div/ul/li/a[text()='Logout']")
    CART_BUTTON = (By.LINK_TEXT, "Checkout »")


class LiteCart(BasePage):

    def get_duck_regular_price(self):
        return self.find_element(LiteCartLocators.REGULAR_PRICE_LOCATOR, time=2).text

    def open_cart(self):
        self.find_element(LiteCartLocators.CART_BUTTON).click()

    def get_duck_data(self):
        reg_price_elem = self.find_element(LiteCartLocators.REGULAR_PRICE_LOCATOR)
        camp_price_elem = self.find_element(LiteCartLocators.CAMPAIGNS_PRICE_LOCATOR)

        duck_data = {
                "regular_price": reg_price_elem.text,
                "campaigns_price": camp_price_elem.text,
                "regular_tag_name": reg_price_elem.get_attribute('tag_name'),
                "campaigns_tag_name": camp_price_elem.get_attribute('tag_name'),
                "regular_price_main_page_color": get_rgb(reg_price_elem.value_of_css_property('color')),
                "campaigns_price_main_page_color": get_rgb(camp_price_elem.value_of_css_property('color')),
                "css_class_reg_price_main_page": reg_price_elem.get_attribute("class"),
                "css_class_camp_price_main_page": camp_price_elem.get_attribute("class"),
                "font_size_reg_price": float(reg_price_elem.value_of_css_property("font-size").replace('px', '')),
                "font_size_camp_price": float(camp_price_elem.value_of_css_property("font-size").replace('px', ''))
        }
        return duck_data

    def login(self, user_email, user_pwd):
        self.driver.find_element(LiteCartLocators.USERNAME_INPUT_LOCATOR).send_keys(user_email)
        self.driver.find_element(LiteCartLocators.PASSWORD_INPUT_LOCATOR).send_keys(user_pwd)
        return self.find_element(LiteCartLocators.LOGIN_BUTTON_LOCATOR, time=5).click()

    def logout(self):
        return self.find_element(LiteCartLocators.LOGOUT_BUTTON_LOCATOR, time=5).click()

    def get_first_duck(self):
        most_popular_block = self.driver.find_element_by_id("box-most-popular")
        first_duck = most_popular_block.find_elements_by_class_name('link')[0]
        return first_duck

    def buy_ducks(self, quantity_ducks: int):
        for i in range(1, quantity_ducks + 1):
            self.get_first_duck().click()
            try:
                select_size = Select(self.driver.find_element_by_name("options[Size]"))
                select_size.select_by_value("Large")
            except NoSuchElementException:
                pass
            self.driver.find_element_by_name("add_cart_product").click()
            wait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "quantity"), str(i)))
            self.go_to_site()

    def remove_ducks_from_cart(self):
        remove_buttons = self.driver.find_elements_by_name("remove_cart_item")
        find_not_empty_rows_xpath = "*//div[@id='order_confirmation-wrapper']/table/tbody/tr"
        empty_cart_xpath = "*//div[@id='checkout-cart-wrapper']/p/em[text()='There are no items in your cart.']"
        for i in range(len(remove_buttons)):
            order_table_rows = self.driver.find_elements_by_xpath(find_not_empty_rows_xpath)
            # если утка не последняя - жждем появление иконки для остановки карусели и кликаем
            if i != len(remove_buttons) - 1:
                time.sleep(1)
                # wait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "shortcuts")))
                self.driver.find_element_by_class_name("shortcuts").click()
            wait(self.driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "remove_cart_item"))).click()
            time.sleep(1)
            if i == len(remove_buttons) - 1 and len(self.driver.find_elements_by_xpath(empty_cart_xpath)) == 1:
                pass
            else:
                wait(self.driver, 10).until(
                    lambda driver: len(self.driver.find_elements(By.XPATH, find_not_empty_rows_xpath)) ==
                    len(order_table_rows) - 1
                )
