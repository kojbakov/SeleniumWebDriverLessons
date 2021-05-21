from selenium.webdriver.common.keys import Keys


def test_login(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin", Keys.TAB)
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    assert driver.find_element_by_id("box-apps-menu-wrapper").is_displayed()