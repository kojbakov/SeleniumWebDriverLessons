import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome(executable_path="./drivers/chromedriver")
    yield driver
    driver.quit()


def test_example(driver):
    driver.get("https://www.google.com/")
    driver.find_element_by_name("q").send_keys("webdriver", Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))


