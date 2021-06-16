from Pages.LiteCartAdminPage import LiteCartAdmin
from selenium.webdriver.common.by import By
import selenium.common.exceptions as sel_exc
from SysFunctions.sys_func import get_all_href_from_ul
from SysFunctions.sys_func import is_list_in_alphabet_order
from selenium.webdriver.common.keys import Keys
import pytest
import time
import os
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wait



@pytest.mark.skip('skip example test')
def test_admin_panel_on_h1_exist(chrome_driver):
    """ 1) входит в панель администратора http://localhost/litecart/admin
        2) прокликивает последовательно все пункты меню слева, включая вложенные пункты
        3) для каждой страницы проверяет наличие заголовка (то есть элемента с тегом h1)"""

    # Логин
    test_page = LiteCartAdmin(chrome_driver)
    test_page.go_to_site("http://localhost/litecart/admin/")
    test_page.login("admin", "admin")
    # Проверка, что логин успешен
    assert test_page.is_user_auth()
    # Получение элементов списка из пунктов меню слева
    element_list = test_page.get_admin_panel().find_elements_by_tag_name("li")
    # Получение всех ссылок из списка пунктов меню
    item_links = get_all_href_from_ul(element_list)
    # Итерация по списку ссылок, включая вложенные пункты с проверкой отображения h1
    for link in item_links:
        test_page.go_to_site(link)
        assert test_page.find_element((By.TAG_NAME, 'h1')).is_displayed()
        try:
            item_panel = chrome_driver.find_element_by_class_name("docs")
            sub_elements_list = item_panel.find_elements_by_tag_name("li")
            all_sub_links = get_all_href_from_ul(sub_elements_list)
            for sub_elem in all_sub_links:
                test_page.go_to_site(sub_elem)
                assert test_page.find_element((By.TAG_NAME, 'h1')).is_displayed()
        except sel_exc.NoSuchElementException as e:
            print("Element has no sub_links")


@pytest.mark.parametrize("test_url, geo_value_index, xpath_expr, geo_attr",
                         # 1-ая часть задания
                         [('http://localhost/litecart/admin/?app=countries&doc=countries', # урл для проверки
                          5,                                                               # столбец с кол-вом гео-зон
                          ".//input[starts-with(@name, 'zones[') and contains(@name, '[name]') ]", # xpath для отбора
                           'value'),                                                       # атрибут для отбора
                          # 2-ая часть задания
                          ('http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones',
                           3,
                           ".//select[contains(@name, '[zone_code]')]/option[@selected='selected']",
                           'text')])
def test_countries_and_geo_zones_alphabet_order(chrome_driver, test_url, geo_value_index, xpath_expr, geo_attr):
    """ 1) на странице http://localhost/litecart/admin/?app=countries&doc=countries
        а) проверяется, что страны расположены в алфавитном порядке
        б) для тех стран, у которых количество зон отлично от нуля --
        открывается страницу этой страны и там проверяется, что зоны расположены в алфавитном порядке
        2) на странице http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones
        заходит в каждую из стран и проверяет, что зоны расположены в алфавитном порядке
        """
    # Логин
    test_page = LiteCartAdmin(chrome_driver)
    test_page.go_to_site(test_url)
    # если пользователь не залогинен - логинимся
    if not test_page.is_user_auth():
        test_page.login("admin", "admin")
    # Проверка, что логин успешен
    assert test_page.is_user_auth()
    # Получение таблицы стран
    countries_table = test_page.find_element((By.CLASS_NAME, "dataTable"))
    urls_with_few_geo_zones = []
    countries_list = []
    # Отбор всех названий стран
    for country in countries_table.find_elements_by_class_name("row"):
        country_link = country.find_element_by_tag_name("a")
        country_name = country_link.text
        countries_list.append(country_name)
        number_geo_zones = int(country.find_elements_by_tag_name("td")[geo_value_index].text)
        if number_geo_zones > 0:
            urls_with_few_geo_zones.append(country_link.get_attribute('href'))
    # Проверка того, что названия стран расположены в алфовитном порядке
    assert is_list_in_alphabet_order(countries_list)
    # Отбор всех названий гео-зон на страницах стран
    for url in urls_with_few_geo_zones:
        test_page.go_to_site(url)
        geo_zones_table = test_page.find_element((By.ID, "table-zones"))
        all_geo_zones_names = [geo.get_attribute(geo_attr) for geo in geo_zones_table.find_elements_by_xpath(xpath_expr)]
        print(all_geo_zones_names)
        # Проверка того, что названия гео-зон расположены в алфовитном порядке
        assert is_list_in_alphabet_order(all_geo_zones_names)


def test_add_some_duck(chrome_driver):
    """Сделайте сценарий для добавления нового товара (продукта) в учебном приложении litecart (в админке).
    """
    # Логин
    chrome_driver.implicitly_wait(10)
    test_page = LiteCartAdmin(chrome_driver)
    test_page.go_to_site("http://localhost/litecart/admin/")
    test_page.login("admin", "admin")
    # Проверка, что логин успешен
    assert test_page.is_user_auth()
    item_panel = chrome_driver.find_element_by_id("box-apps-menu")
    catalog_span = item_panel.find_element_by_xpath(".//span[@class='name' and text()='Catalog']")
    catalog_link = catalog_span.find_element_by_xpath("./..").get_attribute('href')
    chrome_driver.get(catalog_link)
    catalog_edit = chrome_driver.find_element_by_css_selector("a[href*='edit_product']").get_attribute('href')
    chrome_driver.get(catalog_edit)
    chrome_driver.find_element_by_name("name[en]").send_keys("New test product " + datetime.now().strftime("%H%M%S"))
    chrome_driver.find_element_by_name("code").send_keys("Test code")
    for gender in chrome_driver.find_elements_by_name("product_groups[]"):
        gender.click()
    chrome_driver.find_element_by_name("quantity").send_keys("1000")
    upload_img = chrome_driver.find_element_by_name("new_images[]")
    upload_img.send_keys(os.getcwd()+"/duck.png")
    chrome_driver.find_element_by_name("date_valid_from").send_keys(datetime.now().strftime("%d.%m.%Y"))
    tomorrow_date = (datetime.now() + timedelta(1)).strftime("%d.%m.%Y")
    chrome_driver.find_element_by_name("date_valid_to").send_keys(tomorrow_date)
    chrome_driver.find_element_by_link_text("Information").click()
    select_manufacturer = Select(chrome_driver.find_element_by_name("manufacturer_id"))
    select_manufacturer.select_by_value("1")
    chrome_driver.find_element_by_name("keywords").send_keys("test")
    chrome_driver.find_element_by_name("short_description[en]").send_keys("Short description test")
    chrome_driver.find_element_by_css_selector("div.trumbowyg-editor").send_keys("Description test")
    chrome_driver.find_element_by_name("head_title[en]").send_keys("Head title test")
    chrome_driver.find_element_by_name("meta_description[en]").send_keys("Meta description test")
    chrome_driver.find_element_by_link_text("Data").click()
    chrome_driver.find_element_by_name("sku").send_keys("Sku test " + datetime.now().strftime("%H%M%S"))
    chrome_driver.find_element_by_name("gtin").send_keys("Gtin test " + datetime.now().strftime("%H%M%S"))
    chrome_driver.find_element_by_name("taric").send_keys("Taric test " + datetime.now().strftime("%H%M%S"))
    chrome_driver.find_element_by_name("weight").send_keys("5")
    chrome_driver.find_element_by_name("dim_x").send_keys("1")
    chrome_driver.find_element_by_name("dim_y").send_keys("2")
    chrome_driver.find_element_by_name("dim_z").send_keys("3")
    chrome_driver.find_element_by_name("attributes[en]").send_keys("test attr")
    chrome_driver.find_element_by_name("save").click()


def test_link_in_new_tab(chrome_driver):
    test_page = LiteCartAdmin(chrome_driver)
    test_page.go_to_site("http://localhost/litecart/admin/")
    test_page.login("admin", "admin")
    test_page.go_to_site("http://localhost/litecart/admin/?app=countries&doc=countries")
    chrome_driver.find_element_by_class_name("button").click()
    external_links = chrome_driver.find_elements_by_class_name("fa-external-link")
    for link in external_links:
        main_window = chrome_driver.current_window_handle
        old_windows = chrome_driver.window_handles
        link.click()
        new_window = wait(chrome_driver, 10).until(
            lambda chrome_driver: chrome_driver.window_handles != old_windows
        )
        if new_window:
            old_windows = chrome_driver.window_handles
            chrome_driver.switch_to_window(old_windows[-1])
            assert main_window != chrome_driver.current_window_handle
            chrome_driver.close()
            chrome_driver.switch_to_window(main_window)


def test_for_errors_in_logs(chrome_driver):
    """Сценарий проверяет, не появляются ли в логе браузера сообщения при открытии страниц в
     учебном приложении, а именно -- страниц товаров в каталоге в административной панели"""
    test_page = LiteCartAdmin(chrome_driver)
    test_page.go_to_site("http://localhost/litecart/admin/")
    test_page.login("admin", "admin")
    test_page.go_to_site("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    all_rows = chrome_driver.find_elements_by_css_selector("table.dataTable tr.row")
    all_duck_links = []
    for row in all_rows:
        link_row = row.find_element_by_css_selector('a').get_attribute('href')
        # почему-то не сработал поиск через a[href*='edit_product']"
        if "edit_product" in link_row:
            all_duck_links.append(link_row)
    for link in all_duck_links:
        chrome_driver.get(link)
        wait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
        browser_logs = chrome_driver.get_log("browser")
        if len(browser_logs) > 0:
            for l in browser_logs:
                assert l['level'] not in ['WARNING', 'SEVERE'], l['message']

