from selenium.webdriver.common.by import By

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
