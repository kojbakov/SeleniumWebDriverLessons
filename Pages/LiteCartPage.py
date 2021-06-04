from .BaseApp import BasePage
from selenium.webdriver.common.by import By
from SysFunctions.sys_func import get_rgb


class LiteCartLocators:
    REGULAR_PRICE_LOCATOR = (By.CLASS_NAME, 'regular-price')
    CAMPAIGNS_PRICE_LOCATOR = (By.CLASS_NAME, 'campaign-price')
    # inputs
    USERNAME_INPUT_LOCATOR = (By.NAME, "email")
    PASSWORD_INPUT_LOCATOR = (By.NAME, "password")
    # buttons
    LOGIN_BUTTON_LOCATOR = (By.NAME, "login")
    LOGOUT_BUTTON_LOCATOR = (By.XPATH, "//*[@id='box-account']/div/ul/li/a[text()='Logout']")


class LiteCart(BasePage):

    def get_duck_regular_price(self):
        return self.find_element(LiteCartLocators.REGULAR_PRICE_LOCATOR, time=2).text

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
