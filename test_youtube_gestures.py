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
        self.driver.__class__ = type("ExtendedDriver", (self.driver.__class__, ActionHelpers), {})

    def test_scroll(self):
        origin = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Home']"))
        )
        destination = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Trending']"))
        )
        self.driver.scroll(origin, destination, duration=600)
        assert destination.is_displayed()

    def test_drag_and_drop(self):
        video_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((MobileBy.XPATH, "//*[@resource-id='com.google.android.youtube:id/thumbnail']"))
        )
        if len(video_elements) > 1:
            origin = video_elements[0]
            destination = video_elements[1]
            self.driver.drag_and_drop(origin, destination, pause=0.5)
            assert origin.is_displayed()
        else:
            pytest.skip("Недостаточно элементов видео для теста drag_and_drop")

    def test_tap(self):
        search_icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search"))
        )
        location = search_icon.location
        size = search_icon.size
        center_x = int(location['x'] + size['width'] / 2)
        center_y = int(location['y'] + size['height'] / 2)
        self.driver.tap([(center_x, center_y)], duration=500)
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.ID, "com.google.android.youtube:id/search_edit_text"))
        )
        assert search_input.is_displayed()

    def test_swipe(self):
        size = self.driver.get_window_size()
        start_x = int(size['width'] / 2)
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration=800)
        video = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@resource-id='com.google.android.youtube:id/thumbnail']"))
        )
        assert video.is_displayed()

    def test_flick(self):
        size = self.driver.get_window_size()
        start_x = int(size['width'] * 0.9)
        end_x = int(size['width'] * 0.1)
        y = int(size['height'] * 0.95)  
        self.driver.flick(start_x, y, end_x, y)
        library_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((MobileBy.XPATH, "//*[@text='Library']"))
        )
        assert library_tab.is_displayed()
