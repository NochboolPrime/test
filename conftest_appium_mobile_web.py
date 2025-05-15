import pytest
from appium import webdriver

@pytest.fixture(scope="module")
def driver():
    desired_caps = {
       "platformName": "Android",
       "deviceName": "Android Emulator",  # Убедитесь, что эмулятор запущен
       "automationName": "UiAutomator2",
       "browserName": "Chrome",           # Используем мобильный браузер
       "noReset": True
    }
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()
