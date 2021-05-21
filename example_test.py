from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from conftest import driver
import pytest


@pytest.mark.skip('skip example test')
def test_example(driver):
    driver.get("https://www.google.com/")
    driver.find_element_by_name("q").send_keys("webdriver", Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))


