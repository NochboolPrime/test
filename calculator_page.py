from appium.webdriver.common.mobileby import MobileBy

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    def press_digit(self, digit):
        """
        Нажать кнопку с цифрой. digit — строка, например, "2"
        """
        locator = (MobileBy.ID, f"com.google.android.calculator:id/digit_{digit}")
        self.driver.find_element(*locator).click()

    def press_operator(self, operator):
        """
        Нажать оператор. operator – один из символов: "+", "-", "*", "/"
        """
        ops = {
            "+": "com.google.android.calculator:id/op_add",
            "-": "com.google.android.calculator:id/op_sub",
            "*": "com.google.android.calculator:id/op_mul",
            "/": "com.google.android.calculator:id/op_div"
        }
        locator = (MobileBy.ID, ops[operator])
        self.driver.find_element(*locator).click()

    def press_equals(self):
        """
        Нажать кнопку "="
        """
        locator = (MobileBy.ID, "com.google.android.calculator:id/eq")
        self.driver.find_element(*locator).click()

    def press_clear(self):
        """
        Нажать кнопку "C" (очистка).
        Ресурсный id может быть различным, здесь указан один из вариантов.
        """
        locator = (MobileBy.ID, "com.google.android.calculator:id/clr")
        self.driver.find_element(*locator).click()

    def get_result(self):
        """
        Получить результат вычисления.
        Обратите внимание, что у разных версий калькулятора ресурсный id может различаться.
        """
        locator = (MobileBy.ID, "com.google.android.calculator:id/result_final")
        return self.driver.find_element(*locator).text
