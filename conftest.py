import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def chrome_driver():
    driver = webdriver.Chrome(executable_path="./drivers/chromedriver")
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def safari_driver():
    driver = webdriver.Safari(executable_path="./drivers/safaridriver")
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def firefox_driver():
    driver = webdriver.Firefox(executable_path="./drivers/geckodriver")
    yield driver
    driver.quit()


@pytest.fixture(scope="session", params=[
    (webdriver.Chrome, "./drivers/chromedriver"),
    (webdriver.Safari, "./drivers/safaridriver"),
    (webdriver.Firefox, "./drivers/geckodriver")
])
def all_drivers(request):
    driver = request.param[0](executable_path=request.param[1])
    yield driver
    driver.quit()
