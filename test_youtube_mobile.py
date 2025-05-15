# test_youtube_mobile.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("driver")
class TestMobileYouTube:
    def test_homepage_load(self, driver):
        driver.get("https://m.youtube.com")
        WebDriverWait(driver, 10).until(EC.title_contains("YouTube"))
        assert "YouTube" in driver.title

    def test_search_video(self, driver):
        driver.get("https://m.youtube.com")
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Search')]"))
        )
        search_button.click()
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        search_input.send_keys("music")
        search_input.submit()
        WebDriverWait(driver, 10).until(EC.url_contains("search"))
        assert "music" in driver.page_source.lower()

    def test_scroll_down(self, driver):
        driver.get("https://m.youtube.com")
        initial_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.body.scrollHeight") > initial_height
        )
        new_height = driver.execute_script("return document.body.scrollHeight")
        assert new_height > initial_height

    def test_navigate_to_trending(self, driver):
        driver.get("https://m.youtube.com")
        trending_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Trending"))
        )
        trending_link.click()
        WebDriverWait(driver, 10).until(EC.url_contains("trending"))
        assert "Trending" in driver.page_source

    def test_open_video(self, driver):
        driver.get("https://m.youtube.com")
        video = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/watch')]"))
        )
        video.click()
        WebDriverWait(driver, 10).until(EC.url_contains("watch"))
        video_player = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        assert video_player.is_displayed()
