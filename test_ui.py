import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

chromedriver_path = "C:\\Users\\Даниил\\Downloads\\chromedriver-win64\\chromedriver.exe"

@pytest.fixture(scope="module")
def driver():
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_click_product(driver):
    driver.get('https://demo.opencart.com/')
    product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[1]/a/img'))
    )
    product.click()
    assert "Your Store" in driver.title

def test_switch_product_images(driver):
    driver.get('https://demo.opencart.com/')
    product = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/div[1]/a/img'))
    )
    product.click()
    next_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/ul[1]/li[2]/a/img'))
    )
    next_image.click()
    assert driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/ul[1]/li[2]/a/img').is_displayed()

def test_change_currency(driver):
    driver.get('https://demo.opencart.com/')
    currency = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-currency"]/div/button'))
    )
    currency.click()
    usd = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-currency"]/div/ul/li[1]/button'))
    )
    usd.click()
    currency.click()
    eur = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-currency"]/div/ul/li[2]/button'))
    )
    eur.click()
    assert "€" in driver.page_source

def test_navigate_to_pc_category(driver):
    driver.get('https://demo.opencart.com/')
    menu_pc = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'PC (0)'))
    )
    menu_pc.click()
    assert "There are no products to list in this category." in driver.page_source

def test_registration(driver):
    driver.get('https://demo.opencart.com/')
    my_account = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-links"]/ul/li[2]/a'))
    )
    my_account.click()
    register = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-links"]/ul/li[2]/ul/li[1]/a'))
    )
    register.click()
    driver.find_element(By.ID, 'input-firstname').send_keys('Даниил')
    driver.find_element(By.ID, 'input-lastname').send_keys('Иванов')
    driver.find_element(By.ID, 'input-email').send_keys('test@example.com')
    driver.find_element(By.ID, 'input-telephone').send_keys('1234567890')
    driver.find_element(By.ID, 'input-password').send_keys('password123')
    driver.find_element(By.ID, 'input-confirm').send_keys('password123')
    driver.find_element(By.NAME, 'agree').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/div/div/input[2]').click()
    assert "Your Account Has Been Created!" in driver.page_source

def test_search(driver):
    driver.get('https://demo.opencart.com/')
    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'search'))
    )
    search.send_keys('Test')
    driver.find_element(By.XPATH, '//*[@id="search"]/span/button').click()
    assert "Search - Test" in driver.title
