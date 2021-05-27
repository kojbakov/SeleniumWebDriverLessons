import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFOptions


@pytest.fixture(scope="session")
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def safari_driver():
    driver = webdriver.Safari()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def firefox_driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def firefox_esr_driver():
    options = FFOptions()
    options.binary_location = "/Applications/FirefoxESR45.app/Contents/MacOS/firefox-bin"
    driver = webdriver.Firefox(firefox_options=options, capabilities={"marionette": False})
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def firefox_nightly_driver():
    options = FFOptions()
    options.binary_location = "/Applications/Firefox Nightly.app/Contents/MacOS/firefox-bin"
    driver = webdriver.Firefox(firefox_options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", params=[
    webdriver.Chrome,
    webdriver.Safari,
    webdriver.Firefox,
])
def all_drivers(request):
    driver = request.param()
    yield driver
    driver.quit()
