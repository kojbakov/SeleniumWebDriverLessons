from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest


@pytest.mark.skip('skip example test')
def test_login(chrome_driver):
    chrome_driver.get("http://localhost/litecart/admin/")
    chrome_driver.find_element_by_name("username").send_keys("admin", Keys.TAB)
    chrome_driver.find_element_by_name("password").send_keys("admin")
    chrome_driver.find_element_by_name("login").click()
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu-wrapper")))


@pytest.mark.skip('skip example test')
def test_login_with_cookies(chrome_driver):
    """Куки не куки("""
    chrome_driver = webdriver.Chrome()
    chrome_driver.get("http://localhost/litecart/admin/")
    chrome_driver.find_element_by_name("username").send_keys("admin", Keys.TAB)
    chrome_driver.find_element_by_name("password").send_keys("admin")
    chrome_driver.find_element_by_name("login").click()
    WebDriverWait(chrome_driver, 5).until(EC.presence_of_element_located((By.ID, "box-apps-menu-wrapper")))
    all_cookies = chrome_driver.get_cookies()
    chrome_driver.quit()
    new_instance_driver = chrome_driver
    new_instance_driver.get("http://localhost/litecart/admin/")
    for cookie in all_cookies:
        #print(cookie)
        new_instance_driver.add_cookie(cookie)
