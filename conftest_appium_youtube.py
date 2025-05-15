# conftest_appium_youtube.py
import pytest
from appium import webdriver

YOUTUBE_APK_PATH = "C:\\Users\\Даниил\\Downloads\\YouTube.apk"

@pytest.fixture(scope="module")
def driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",       # Убедитесь, что эмулятор запущен
        "automationName": "UiAutomator2",
        "app": YOUTUBE_APK_PATH,                # Путь к APK-файлу YouTube
        "noReset": True
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()
