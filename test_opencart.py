import pytest
import logging
import allure
from pages import HomePage, ProductPage, RegisterPage, CartPage

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@pytest.mark.usefixtures("driver")
class TestOpenCart:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.driver.get("https://demo.opencart.com/")
        self.home_page = HomePage(driver)
        self.product_page = ProductPage(driver)
        self.register_page = RegisterPage(driver)
        self.cart_page = CartPage(driver)

    @allure.feature("Тестирование списка желаемого")
    @allure.story("Добавление iPhone в список желаемого")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_wishlist(self):
        logging.info("Начинаем тест: добавление iPhone в список желаемого")
        self.home_page.search_for("iPhone")
        self.product_page.add_to_wishlist()
        logging.info("Тест успешно завершен")

    @allure.feature("Тестирование корзины")
    @allure.story("Добавление камеры в корзину")
    def test_add_camera_to_cart(self):
        logging.info("Начинаем тест: добавление камеры в корзину")
        self.home_page.search_for("camera")
        self.product_page.add_to_cart()
        logging.info("Камера успешно добавлена")

    @allure.feature("Тестирование написания отзывов")
    @allure.story("Написание отзыва к iPhone")
    def test_write_review(self):
        logging.info("Начинаем тест: написание отзыва на iPhone")
        self.home_page.search_for("iPhone")
        self.product_page.write_review()
        logging.info("Открыта форма написания отзыва")
