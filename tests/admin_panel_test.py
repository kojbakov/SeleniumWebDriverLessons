from Pages.LiteCartAdminPage import LiteCartAdmin
from selenium.webdriver.common.by import By
import selenium.common.exceptions as sel_exc
from SysFunctions.sys_func import get_all_href_from_ul
from SysFunctions.sys_func import is_list_in_alphabet_order
import pytest


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
