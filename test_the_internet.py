import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

BASE_URL = "https://the-internet.herokuapp.com/"

@pytest.mark.usefixtures("driver")
class TestTheInternet:
    def test_form_authentication_invalid(self, driver):
        """
        Тест Form Authentication:
        Переход на страницу логина, ввод неверных учетных данных и проверка сообщения об ошибке.
        """
        driver.get(BASE_URL + "login")
        driver.find_element(By.ID, "username").send_keys("wronguser")
        driver.find_element(By.ID, "password").send_keys("wrongpass")
        driver.find_element(By.CSS_SELECTOR, "button.radius").click()
        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        assert "Your username is invalid!" in error.text

    def test_checkboxes(self, driver):
        """
        Тест Checkboxes:
        Переход на страницу, проверка состояния чекбоксов и изменение состояния.
        """
        driver.get(BASE_URL + "checkboxes")
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        assert len(checkboxes) == 2
        if not checkboxes[0].is_selected():
            checkboxes[0].click()
            assert checkboxes[0].is_selected()
        else:
            checkboxes[1].click()
            assert checkboxes[1].is_selected()

    def test_dropdown(self, driver):
        """
        Тест Dropdown:
        Переход на страницу Dropdown, выбор Option 2 и проверка выбранного значения.
        """
        driver.get(BASE_URL + "dropdown")
        dropdown_element = driver.find_element(By.ID, "dropdown")
        select = Select(dropdown_element)
        select.select_by_visible_text("Option 2")
        selected_option = select.first_selected_option
        assert selected_option.text == "Option 2"

    def test_js_alert(self, driver):
        """
        Тест JavaScript Alert:
        Переход на страницу JavaScript Alerts, клик по кнопке "Click for JS Alert",
        принятие алерта и проверка результата.
        """
        driver.get(BASE_URL + "javascript_alerts")
        driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()
        result = driver.find_element(By.ID, "result").text
        assert "You successfuly clicked an alert" in result

    def test_js_confirm(self, driver):
        """
        Тест JavaScript Confirm:
        Клик по кнопке "Click for JS Confirm", отмена алерта и проверка результата.
        """
        driver.get(BASE_URL + "javascript_alerts")
        driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.dismiss()
        result = driver.find_element(By.ID, "result").text
        assert "You clicked: Cancel" in result

    def test_dynamic_loading(self, driver):
        """
        Тест Dynamic Loading:
        Переход на страницу Dynamic Loading Example 1, запуск загрузки и ожидание результата.
        """
        driver.get(BASE_URL + "dynamic_loading/1")
        driver.find_element(By.CSS_SELECTOR, "#start button").click()
        finish_elem = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )
        assert "Hello World!" in finish_elem.text

    def test_file_upload(self, driver):
        """
        Тест File Upload:
        Переход на страницу File Upload, загрузка файла и проверка успешной загрузки.
        """
        driver.get(BASE_URL + "upload")
        file_path = os.path.join(os.getcwd(), "test_upload.txt")
        with open(file_path, "w") as f:
            f.write("This is a test file for upload.")
        upload_input = driver.find_element(By.ID, "file-upload")
        upload_input.send_keys(file_path)
        driver.find_element(By.ID, "file-submit").click()
        header_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        ).text
        assert "File Uploaded!" in header_text
        os.remove(file_path)

    def test_drag_and_drop(self, driver):
        """
        Тест Drag and Drop:
        Переход на страницу Drag and Drop, перетаскивание элемента A на элемент B и проверка смены позиций.
        Из-за особенностей реализации DnD на этой странице используется JavaScript-решение.
        """
        driver.get(BASE_URL + "drag_and_drop")
        source = driver.find_element(By.XPATH, "//*[@id='columns']/div[1]")
        target = driver.find_element(By.XPATH, "//*[@id='columns']/div[2]")
        js_drag_drop = """
        function simulateDragDrop(sourceNode, destinationNode) {
            var EVENT_TYPES = {
                DRAG_START: 'dragstart',
                DROP: 'drop',
                DRAG_END: 'dragend'
            }
            function createCustomEvent(type) {
                var event = new CustomEvent("CustomEvent");
                event.initCustomEvent(type, true, true, null);
                event.dataTransfer = {
                    data: {},
                    setData: function(key, value) {
                        this.data[key] = value;
                    },
                    getData: function(key) {
                        return this.data[key];
                    }
                };
                return event;
            }
            function dispatchEvent(node, type, event) {
                if (node.dispatchEvent) {
                    return node.dispatchEvent(event);
                }
                if (node.fireEvent) {
                    return node.fireEvent("on" + type, event);
                }
            }
            var dragStartEvent = createCustomEvent(EVENT_TYPES.DRAG_START);
            dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START, dragStartEvent);
            var dropEvent = createCustomEvent(EVENT_TYPES.DROP);
            dropEvent.dataTransfer = dragStartEvent.dataTransfer;
            dispatchEvent(destinationNode, EVENT_TYPES.DROP, dropEvent);
            var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
            dragEndEvent.dataTransfer = dragStartEvent.dataTransfer;
            dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, dragEndEvent);
        }
        simulateDragDrop(arguments[0], arguments[1]);
        """
        driver.execute_script(js_drag_drop, source, target)
        col1_text = driver.find_element(By.XPATH, "//*[@id='columns']/div[1]").text
        col2_text = driver.find_element(By.XPATH, "//*[@id='columns']/div[2]").text
        assert "B" in col1_text or "A" in col2_text

    def test_infinite_scroll(self, driver):
        """
        Тест Infinite Scroll:
        Переход на страницу Infinite Scroll, скролл вниз и проверка появления нового контента.
        """
        driver.get(BASE_URL + "infinite_scroll")
        paragraphs = driver.find_elements(By.CSS_SELECTOR, ".jscroll-added p")
        initial_count = len(paragraphs)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        new_paragraphs = driver.find_elements(By.CSS_SELECTOR, ".jscroll-added p")
        assert len(new_paragraphs) > initial_count

    def test_context_menu(self, driver):
        """
        Тест Context Menu:
        Переход на страницу Context Menu, выполнение правого клика по области и проверка текста в алерте.
        """
        driver.get(BASE_URL + "context_menu")
        hotspot = driver.find_element(By.ID, "hot-spot")
        ActionChains(driver).context_click(hotspot).perform()
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        assert "You selected a context menu" in alert_text
