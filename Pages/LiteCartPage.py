from .BaseApp import BasePage
from selenium.webdriver.common.by import By


class LiteCartLocators:
    REGULAR_PRICE_LOCATOR = (By.CLASS_NAME, 'regular-price')
    CAMPAIGNS_PRICE_LOCATOR = (By.CLASS_NAME, 'campaign-price')


class LiteCart(BasePage):

    def get_duck_regular_price(self):
        return self.find_element(LiteCartLocators.REGULAR_PRICE_LOCATOR, time=2).text

    def get_duck_data(self):
        reg_price_elem = self.find_element(LiteCartLocators.REGULAR_PRICE_LOCATOR)
        camp_price_elem = self.find_element(LiteCartLocators.CAMPAIGNS_PRICE_LOCATOR)
        duck_data = {
                "regular_price": reg_price_elem.text,
                "campaigns_price": camp_price_elem.text,
                "regular_price_main_page_color": reg_price_elem.value_of_css_property('color'),
                "campaigns_price_main_page_color": camp_price_elem.value_of_css_property('color'),
                "css_class_reg_price_main_page": reg_price_elem.get_attribute("class"),
                "css_class_camp_price_main_page": camp_price_elem.get_attribute("class")
        }
        return duck_data
