# test_youtube_gestures.py
import pytest
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gesture_extensions.action_helpers import ActionHelpers

@pytest.mark.usefixtures("driver")
class TestYouTubeGestures:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        # Расширяем драйвер, добавляя методы жестов из ActionHelpers
        self.driver.__class__ = type("ExtendedDriver", (self.driver.__class__, ActionHelpers), {})

    def test_scroll(self):
        # Ждем появления элемента "Home" и "Trending" на нижней панели
        origin = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Home']"))
        )
        destination = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Trending']"))
        )
        self.driver.scroll(origin, destination, duration=600)
        # Проверяем, что элемент назначения виден
        assert destination.is_displayed()

    def test_drag_and_drop(self):
        # Пытаемся найти несколько миниатюр видео в главном ленте
        video_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((MobileBy.XPATH, "//*[@resource-id='com.google.android.youtube:id/thumbnail']"))
        )
        if len(video_elements) > 1:
            origin = video_elements[0]
            destination = video_elements[1]
            self.driver.drag_and_drop(origin, destination, pause=0.5)
            # Проверяем, что исходный элемент продолжает отображаться
            assert origin.is_displayed()
        else:
            pytest.skip("Недостаточно элементов видео для теста drag_and_drop")

    def test_tap(self):
        # Находим и тапаем по кнопке поиска (предполагается, что у элемента есть accessibility id "Search")
        search_icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search"))
        )
        location = search_icon.location
        size = search_icon.size
        center_x = int(location['x'] + size['width'] / 2)
        center_y = int(location['y'] + size['height'] / 2)
        self.driver.tap([(center_x, center_y)], duration=500)
        # После нажатия ожидаем, что появится поле ввода поиска
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.ID, "com.google.android.youtube:id/search_edit_text"))
        )
        assert search_input.is_displayed()

    def test_swipe(self):
        # Выполняем вертикальный swipe: от нижней части экрана к верхней
        size = self.driver.get_window_size()
        start_x = int(size['width'] / 2)
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)
        # После swipe ждем появления хотя бы одной миниатюры видео
        video = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='com.google.android.youtube:id/thumbnail']"))
        )
        assert video.is_displayed()

    def test_flick(self):
        # Выполняем быстрый горизонтальный flick по нижней (таббар) области экрана
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.9)
        end_x = int(size['width'] * 0.1)
        y = int(size['height'] * 0.95)  # предполагается, что таббар внизу
        self.driver.flick(start_x, y, end_x, y)
        # Проверяем, что отображается вкладка "Library"
        library_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Library']"))
        )
        assert library_tab.is_displayed()
