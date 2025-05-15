import pytest

def test_selenoid_ui(driver, request):
    executor = request.config.getoption("--executor")
    selenoid_ui_url = f"http://{executor}:8080"
    driver.get(selenoid_ui_url)
    page_source = driver.page_source
    assert "Selenoid" in page_source or "Containers" in page_source, "Selenoid web interface did not load properly"
