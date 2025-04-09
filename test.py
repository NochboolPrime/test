import datetime
import pytest
import logging
import allure
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true")
    parser.addoption("--executor", action="store", default="127.0.0.1")
    parser.addoption("--log_level", action="store", default="INFO")

@pytest.fixture()
def driver(request):
    executor = request.config.getoption("--executor")
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info(
        "===> Test %s started at %s" % (request.node.name, datetime.datetime.now())
    )

    executor_url = f"http://{executor}:4444/wd/hub"

    if browser_name == "chrome":
        options = Options()
        if headless:
            options.add_argument("headless=new")
        options.headless = headless
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.headless = headless
    else:
        raise NotImplemented()

    browser = webdriver.Remote(command_executor=executor_url, options=options)
    allure.attach(
        name=browser.session_id,
        body=json.dumps(browser.capabilities),
        attachment_type=allure.attachment_type.JSON,
    )

    browser.log_level = log_level
    browser.logger = logger
    browser.test_name = request.node.name

    logger.info("Browser %s started" % browser)

    browser.maximize_window()

    def fin():
        browser.quit()
        logger.info(
            "===> Test %s finished at %s" % (request.node.name, datetime.datetime.now())
        )

    request.addfinalizer(fin)
    return browser

def test_create_category(driver):
    driver.get('https://demo.opencart.com/admin/')
    
    # Войти в админ-панель
    driver.find_element(By.ID, 'input-username').send_keys('admin')
    driver.find_element(By.ID, 'input-password').send_keys('password')
    driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div/div[2]/form/div[2]/button').click()

    # Перейти в раздел «Категории»
    driver.get('https://demo.opencart.com/admin/index.php?route=catalog/category')
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/a').click()

    # Заполнить данные категории «Devices»
    driver.find_element(By.ID, 'input-name1').send_keys('Devices')
    driver.find_element(By.ID, 'input-meta-title1').send_keys('Devices Category')
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/button').click()

    assert "Success" in driver.page_source

def test_add_products(driver):
    driver.get('https://demo.opencart.com/admin/index.php?route=catalog/product')
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/a').click()

    # Добавляем 2 мыши
    for name in ['Gaming Mouse', 'Wireless Mouse']:
        driver.find_element(By.ID, 'input-name1').send_keys(name)
        driver.find_element(By.ID, 'input-meta-title1').send_keys(name)
        driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/button').click()

    # Добавляем 2 клавиатуры
    for name in ['Mechanical Keyboard', 'Wireless Keyboard']:
        driver.find_element(By.ID, 'input-name1').send_keys(name)
        driver.find_element(By.ID, 'input-meta-title1').send_keys(name)
        driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/button').click()

    assert "Success" in driver.page_source

def test_search_products(driver):
    driver.get('https://demo.opencart.com/')
    search_box = driver.find_element(By.NAME, 'search')

    for name in ['Gaming Mouse', 'Wireless Mouse', 'Mechanical Keyboard', 'Wireless Keyboard']:
        search_box.clear()
        search_box.send_keys(name)
        driver.find_element(By.XPATH, '//*[@id="search"]/span/button').click()
        assert name in driver.page_source

def test_delete_products(driver):
    driver.get('https://demo.opencart.com/admin/index.php?route=catalog/product')

    for name in ['Gaming Mouse', 'Mechanical Keyboard']:
        search_box = driver.find_element(By.NAME, 'filter_name')
        search_box.clear()
        search_box.send_keys(name)
        driver.find_element(By.XPATH, '//*[@id="button-filter"]').click()

        driver.find_element(By.NAME, 'selected[]').click()
        driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div/button[2]').click()

    assert "Success" in driver.page_source

def test_remaining_products(driver):
    driver.get('https://demo.opencart.com/')
    search_box = driver.find_element(By.NAME, 'search')

    for name in ['Wireless Mouse', 'Wireless Keyboard']:
        search_box.clear()
        search_box.send_keys(name)
        driver.find_element(By.XPATH, '//*[@id="search"]/span/button').click()
        assert name in driver.page_source
