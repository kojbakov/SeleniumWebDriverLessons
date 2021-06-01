from Pages.BaseApp import BasePage
from selenium.webdriver.common.by import By
from Pages.LiteCartPage import LiteCart, LiteCartLocators
import pytest_check as check


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
    # Сравнение
    check.equal(first_duck_title, duck_block_title, "Title is not equal!")
    for key in duck_data_main_page.keys():
        check.equal(duck_data_main_page[key], duck_data_page[key], f"{key} param in not equal")
