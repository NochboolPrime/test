import logging
import allure
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.NAME, "search")
        self.search_button = (By.CLASS_NAME, "btn-default")

    @allure.step("Выполняем поиск товара: {item}")
    def search_for(self, item):
        logging.info(f"Поиск товара: {item}")
        self.driver.find_element(*self.search_box).send_keys(item)
        self.driver.find_element(*self.search_button).click()

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_to_cart_button = (By.ID, "button-cart")
        self.add_to_wishlist_button = (By.XPATH, "//button[@data-original-title='Add to Wish List']")
        self.write_review_button = (By.LINK_TEXT, "Write a review")

    @allure.step("Добавляем товар в корзину")
    def add_to_cart(self):
        logging.info("Добавление товара в корзину")
        self.driver.find_element(*self.add_to_cart_button).click()

    @allure.step("Добавляем товар в список желаемого")
    def add_to_wishlist(self):
        logging.info("Добавление товара в список желаемого")
        self.driver.find_element(*self.add_to_wishlist_button).click()

    @allure.step("Открываем страницу написания отзыва")
    def write_review(self):
        logging.info("Открываем форму написания отзыва")
        self.driver.find_element(*self.write_review_button).click()

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.first_name = (By.ID, "input-firstname")
        self.last_name = (By.ID, "input-lastname")
        self.email = (By.ID, "input-email")
        self.password = (By.ID, "input-password")
        self.confirm_password = (By.ID, "input-confirm")
        self.privacy_policy_checkbox = (By.NAME, "agree")
        self.continue_button = (By.CSS_SELECTOR, ".btn-primary")

    @allure.step("Заполняем форму регистрации: {first_name}, {last_name}, {email}")
    def fill_registration_form(self, first_name, last_name, email, password):
        logging.info(f"Заполнение формы: {first_name} {last_name}, Email: {email}")
        self.driver.find_element(*self.first_name).send_keys(first_name)
        self.driver.find_element(*self.last_name).send_keys(last_name)
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.confirm_password).send_keys(password)
        self.driver.find_element(*self.privacy_policy_checkbox).click()
        self.driver.find_element(*self.continue_button).click()

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.checkout_button = (By.LINK_TEXT, "Checkout")

    @allure.step("Оформляем заказ")
    def go_to_checkout(self):
        logging.info("Переход к оформлению заказа")
        self.driver.find_element(*self.checkout_button).click()
