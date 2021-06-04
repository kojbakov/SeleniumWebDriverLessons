from .BaseApp import BasePage
from selenium.webdriver.common.by import By
import selenium.common.exceptions


class LiteCartAdminLocators:
    # button
    LOCATOR_LOGIN_BUTTON = (By.NAME, "login")
    # inputs
    LOCATOR_USERNAME_INPUT = (By.NAME, "username")
    LOCATOR_PASSWORD_INPUT = (By.NAME, "password")
    # other
    LOCATOR_USER_AUTH = (By.ID, "box-apps-menu-wrapper")


class LiteCartAdmin(BasePage):

    def enter_word(self, word, locator):
        input_field = self.find_element(locator)
        input_field.click()
        input_field.send_keys(word)
        return input_field

    def click_on_login_button(self):
        return self.find_element(LiteCartAdminLocators.LOCATOR_LOGIN_BUTTON, time=2).click()

    def get_admin_panel(self):
        return self.find_element(LiteCartAdminLocators.LOCATOR_USER_AUTH, time=2)

    def login(self, user_email, user_pwd):
        self.enter_word(user_email, LiteCartAdminLocators.LOCATOR_USERNAME_INPUT)
        self.enter_word(user_pwd, LiteCartAdminLocators.LOCATOR_PASSWORD_INPUT)
        return self.find_element(LiteCartAdminLocators.LOCATOR_LOGIN_BUTTON, time=5).click()

    def is_user_auth(self):
        try:
            return self.find_element(LiteCartAdminLocators.LOCATOR_USER_AUTH, time=5).is_displayed()
        except selenium.common.exceptions.TimeoutException as e:
            return False

