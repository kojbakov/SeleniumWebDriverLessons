from Pages.LiteCartAdminPage import LiteCartAdmin
from selenium.webdriver.common.by import By
import selenium.common.exceptions as sel_exc
from SysFunctions.sys_func import get_all_href_from_ul


def test_login(chrome_driver):
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
            print(f"Element has no sub_links")
