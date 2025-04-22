import pytest
from calculator_page import CalculatorPage

def test_addition(driver):
    calc = CalculatorPage(driver)
    calc.press_clear()  
    calc.press_digit("2")
    calc.press_operator("+")
    calc.press_digit("3")
    calc.press_equals()
    result = calc.get_result()
    assert result == "5", f"Expected 5, but got {result}"

def test_subtraction(driver):
    calc = CalculatorPage(driver)
    calc.press_clear()
    calc.press_digit("5")
    calc.press_operator("-")
    calc.press_digit("2")
    calc.press_equals()
    result = calc.get_result()
    assert result == "3", f"Expected 3, but got {result}"

def test_multiplication(driver):
    calc = CalculatorPage(driver)
    calc.press_clear()
    calc.press_digit("4")
    calc.press_operator("*")
    calc.press_digit("6")
    calc.press_equals()
    result = calc.get_result()
    assert result == "24", f"Expected 24, but got {result}"

def test_division(driver):
    calc = CalculatorPage(driver)
    calc.press_clear()
    calc.press_digit("8")
    calc.press_operator("/")
    calc.press_digit("2")
    calc.press_equals()
    result = calc.get_result()
    assert result == "4", f"Expected 4, but got {result}"

def test_clear_function(driver):
    calc = CalculatorPage(driver)
   
    calc.press_digit("9")
    calc.press_operator("+")
    calc.press_digit("1")
    calc.press_clear()
    result = calc.get_result()

    assert result in ["", "0"], f"Expected a cleared result, but got {result}"
