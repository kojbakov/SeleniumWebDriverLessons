from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_login(all_drivers):
    all_drivers.get("http://localhost/litecart/admin/")
    all_drivers.find_element_by_name("username").send_keys("admin", Keys.TAB)
    all_drivers.find_element_by_name("password").send_keys("admin")
    all_drivers.find_element_by_name("login").click()
    WebDriverWait(all_drivers, 10).until(EC.presence_of_element_located((By.ID, "box-apps-menu-wrapper")))



