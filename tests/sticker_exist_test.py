from Pages.BaseApp import BasePage


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
        assert len(duck.find_elements_by_class_name("sticker")) != 1, "Duck stickers != 1!"

