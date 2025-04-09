import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true")
    parser.addoption("--log_level", action="store", default="INFO")

@pytest.fixture()
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info(f"===> Test {request.node.name} started")

    if browser_name == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError("Browser not supported")

    driver.logger = logger

    logger.info(f"Browser {browser_name} started")

    driver.maximize_window()

    def fin():
        driver.quit()
        logger.info(f"===> Test {request.node.name} finished")

    request.addfinalizer(fin)
    return driver