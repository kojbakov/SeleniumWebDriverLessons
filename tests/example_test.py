from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.skip('skip example test')
def test_example(safari_driver):
    safari_driver.get("https://www.google.com/")
    safari_driver.find_element_by_name("q").send_keys("webdriver", Keys.ENTER)
    WebDriverWait(safari_driver, 10).until(EC.title_is("webdriver - Поиск в Google"))


