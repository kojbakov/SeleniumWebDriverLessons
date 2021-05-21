import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome(executable_path="./drivers/chromedriver")
    yield driver
    driver.quit()
