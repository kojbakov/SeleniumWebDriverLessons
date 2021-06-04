from .BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class LiteCartRegistrationLocators:

    # inputs
    TAX_ID_LOCATOR = (By.NAME, "tax_id")
    COMPANY_LOCATOR = (By.NAME, "company")
    FIRST_NAME_LOCATOR = (By.NAME, "firstname")
    LAST_NAME_LOCATOR = (By.NAME, "lastname")
    ADDRESS_1_LOCATOR = (By.NAME, "address1")
    ADDRESS_2_LOCATOR= (By.NAME, "address2")
    POSTCODE_LOCATOR = (By.NAME, "postcode")
    CITY_LOCATOR = (By.NAME, "city")
    STATE_LOCATOR = (By.XPATH, '*//select[@name="zone_code"]')
    EMAIL_LOCATOR = (By.NAME, "email")
    PHONE_LOCATOR = (By.NAME, "phone")
    PASSWORD_LOCATOR = (By.NAME, "password")
    CONFIRM_PASSWORD_LOCATOR = (By.NAME, "confirmed_password")
    COUNTRY_SEARCH_LOCATOR = (By.CLASS_NAME, "select2-search__field")
    USERNAME_INPUT_LOCATOR = (By.NAME, "email")
    PASSWORD_INPUT_LOCATOR = (By.NAME, "password")
    # buttons
    CREATE_ACCOUNT_BUTTON_LOCATOR = (By.NAME, "create_account")
    DROPDOWN_BUTTON_LOCATOR = (By.CLASS_NAME, "select2-selection__arrow")
    LOGIN_BUTTON_LOCATOR = (By.NAME, "login")
    LOGOUT_BUTTON_LOCATOR = (By.XPATH, "//*[@id='box-account']/div/ul/li/a[text()='Logout']")


class LiteCartRegistration(BasePage):

    def get_tax_id(self):
        return self.find_element(LiteCartRegistrationLocators.TAX_ID_LOCATOR, 2)

    def get_company(self):
        return self.find_element(LiteCartRegistrationLocators.COMPANY_LOCATOR, 2)

    def get_first_name(self):
        return self.find_element(LiteCartRegistrationLocators.FIRST_NAME_LOCATOR, 2)

    def get_last_name(self):
        return self.find_element(LiteCartRegistrationLocators.LAST_NAME_LOCATOR, 2)

    def get_address_1(self):
        return self.find_element(LiteCartRegistrationLocators.ADDRESS_1_LOCATOR, 2)

    def get_address_2(self):
        return self.find_element(LiteCartRegistrationLocators.ADDRESS_2_LOCATOR, 2)

    def get_postcode(self):
        return self.find_element(LiteCartRegistrationLocators.POSTCODE_LOCATOR, 2)

    def get_city(self):
        return self.find_element(LiteCartRegistrationLocators.CITY_LOCATOR, 2)

    def get_country(self):
        return self.find_element(LiteCartRegistrationLocators.COUNTRY_SEARCH_LOCATOR, 2)

    def get_state(self):
        return self.find_elements(LiteCartRegistrationLocators.STATE_LOCATOR, 2)

    def get_email(self):
        return self.find_element(LiteCartRegistrationLocators.EMAIL_LOCATOR, 2)

    def get_phone(self):
        return self.find_element(LiteCartRegistrationLocators.PHONE_LOCATOR, 2)

    def get_password(self):
        return self.find_element(LiteCartRegistrationLocators.PASSWORD_LOCATOR, 2)

    def get_confirm_password(self):
        return self.find_element(LiteCartRegistrationLocators.CONFIRM_PASSWORD_LOCATOR, 2)

    def click_create_account_button(self):
        self.find_element(LiteCartRegistrationLocators.CREATE_ACCOUNT_BUTTON_LOCATOR, 5).click()

    def click_dropdown_countries_list(self):
        return self.find_element(LiteCartRegistrationLocators.DROPDOWN_BUTTON_LOCATOR, 2).click()

    def click_states(self):
        return self.find_element(LiteCartRegistrationLocators.STATE_LOCATOR, 2).click()

    def choose_state(self, state):
        customer_form = self.driver.find_element_by_name("customer_form")
        xpath = f".//select[@name='zone_code']/option[text()='{state}']"
        customer_form.find_element_by_xpath(xpath).click()

    def login(self, user_email, user_pwd):
        self.driver.find_element_by_name("email").send_keys(user_email)
        self.driver.find_element_by_name("password").send_keys(user_pwd)
        self.driver.find_element_by_name("login").click()

    def logout(self):
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(LiteCartRegistrationLocators.LOGOUT_BUTTON_LOCATOR))
        logout_button.click()
