from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_login(chrome_driver):
    chrome_driver.get("http://localhost/litecart/admin/")
    chrome_driver.find_element_by_name("username").send_keys("admin", Keys.TAB)
    chrome_driver.find_element_by_name("password").send_keys("admin")
    chrome_driver.find_element_by_name("login").click()
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu-wrapper")))


