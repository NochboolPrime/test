import datetime
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true")
    # Если указан --executor, запускаем удалённо через Selenoid (обычно на порту 4444)
    parser.addoption("--executor", action="store", default="127.0.0.1", help="Selenoid host IP")
    parser.addoption("--log_level", action="store", default="INFO")

@pytest.fixture()
def driver(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    executor = request.config.getoption("--executor")
    log_level = request.config.getoption("--log_level")
    
    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)
    
    logger.info(f"===> Test {request.node.name} started at {datetime.datetime.now()}")

    if executor:
        # Запускаем удалённо через Selenoid
        remote_url = f"http://{executor}:4444/wd/hub"
        if browser_name == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless")
            driver_instance = webdriver.Remote(command_executor=remote_url, options=options)
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver_instance = webdriver.Remote(command_executor=remote_url, options=options)
        else:
            raise ValueError("Browser not supported")
    else:
        # Локальный запуск
        if browser_name == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless")
            driver_instance = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver_instance = webdriver.Firefox(options=options)
        else:
            raise ValueError("Browser not supported")
    
    driver_instance.logger = logger
    logger.info(f"Browser {browser_name} started")
    driver_instance.maximize_window()
    
    def fin():
        driver_instance.quit()
        logger.info(f"===> Test {request.node.name} finished at {datetime.datetime.now()}")
    request.addfinalizer(fin)
    return driver_instance
