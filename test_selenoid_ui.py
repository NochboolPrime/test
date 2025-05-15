import pytest

def test_selenoid_ui(driver, request):
    executor = request.config.getoption("--executor")
    # Selenoid UI обычно работает на порту 8080
    selenoid_ui_url = f"http://{executor}:8080"
    driver.get(selenoid_ui_url)
    # Проверяем, что в коде страницы присутствует слово "Selenoid" или другой ориентир.
    page_source = driver.page_source
    assert "Selenoid" in page_source or "Containers" in page_source, "Selenoid web interface did not load properly"
