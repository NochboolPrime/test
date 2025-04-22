import pytest
from appium import webdriver

@pytest.fixture(scope="module")
def driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Emulator",  
        "appPackage": "com.google.android.calculator",  
        "appActivity": ".Calculator",                   
        "automationName": "UiAutomator2",
        
        "noReset": True
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    yield driver
    driver.quit()
