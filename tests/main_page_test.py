from Pages.BaseApp import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Pages.LiteCartPage import LiteCart, LiteCartLocators
from Pages.LiteCartRegistrationPage import LiteCartRegistration, LiteCartRegistrationLocators
import pytest_check as check
import time
from datetime import datetime
import re

from selenium.webdriver.support.color import Color


def test_duck_sticker(chrome_driver):
    """
    Сценарий проверяет, что у каждого товара на странице http://localhost/litecart/
    имеется ровно один стикер.
    """
    test_page = BasePage(chrome_driver)
    test_page.go_to_site()
    # Получение списка всех товаров
    all_ducks = chrome_driver.find_elements_by_class_name("image-wrapper")
    # Итерация по товарам с проверкой, что у каждого товара ровно один стикер
    for duck in all_ducks:
        assert len(duck.find_elements_by_class_name("sticker")) == 1, "Duck stickers != 1!"


def test_duck_compare(all_drivers):
    """
    Сценарий проверяет, что при клике на товар открывается правильная страница товара в учебном приложении litecart.
    """
    test_page = LiteCart(all_drivers)
    test_page.go_to_site()
    campaigns_block = test_page.find_element((By.ID, "box-campaigns"))
    first_duck = campaigns_block.find_elements_by_class_name('link')[0]
    first_duck_title = first_duck.get_attribute('title')
    first_duck_link = first_duck.get_attribute('href')
    duck_data_main_page = (test_page.get_duck_data())
    test_page.go_to_site(first_duck_link)
    duck_block = test_page.find_element((By.ID, "box-product"))
    duck_block_title = duck_block.find_element_by_class_name('title').text
    duck_data_page = (test_page.get_duck_data())
    # Сравнение заголовков
    check.equal(first_duck_title, duck_block_title, "Title is not equal!")
    for key in duck_data_main_page.keys():
        if key not in [
            "font_size_reg_price",
            "font_size_camp_price",
            "regular_price_main_page_color",
            "campaigns_price_main_page_color"
        ]:
            check.equal(duck_data_main_page[key], duck_data_page[key], f"{key} param in not equal")

    test_pages = [duck_data_main_page, duck_data_page]
    for page in test_pages:
        # Проверка серого цвета обычной цены(r = g = b)
        check.equal(len(set(page["regular_price_main_page_color"])), 1)
        # Проверка красного цвета акционной цены (g и b = 0)
        check.equal(int(page["campaigns_price_main_page_color"][1]), 0)
        check.equal(int(page["campaigns_price_main_page_color"][2]), 0)
        # проверка, что акционная цена крупнее, чем обычная
        check.less(page["font_size_reg_price"], page["font_size_camp_price"])


def test_registration(chrome_driver):
    """
    Сделайте сценарий для регистрации нового пользователя в учебном приложении litecart    """

    test_page = LiteCartRegistration(chrome_driver, "http://localhost/litecart/en/create_account")
    test_page.go_to_site()
    test_page.get_tax_id().send_keys("test tax_id 1")
    test_page.get_company().send_keys("test company")
    test_page.get_first_name().send_keys("test first name")
    test_page.get_last_name().send_keys("test last name")
    test_page.get_address_1().send_keys("test address 1")
    test_page.get_address_2().send_keys("test address 2")
    test_page.get_postcode().send_keys("10001")
    test_page.get_city().send_keys("New York")
    test_page.click_dropdown_countries_list()
    test_page.get_country().send_keys("United States", Keys.ENTER)
    # Иногда падает тут, не находит элемент
    test_page.choose_state("New York")
    # генерация адреса почты
    test_mail = datetime.now().strftime("%H%M%S") + "@testmail.ru"
    test_page.get_email().send_keys(test_mail)
    test_page.get_phone().send_keys("+79781233212")
    test_page.get_password().send_keys("1")
    test_page.get_confirm_password().send_keys("1")
    test_page.click_create_account_button()
    # Нормальные ожидания не сработали(
    time.sleep(1)
    test_page.logout()
    # WebDriverWait(chrome_driver, 10).until(
    #     EC.presence_of_element_located(LiteCartRegistrationLocators.LOGIN_BUTTON_LOCATOR))
    time.sleep(1)
    test_page.login(test_mail, "1")
    test_page.logout()
