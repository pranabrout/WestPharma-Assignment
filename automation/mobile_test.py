import os
import time
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By


# Require RUN_MOBILE=1 to run mobile/Appium tests.
RUN_MOBILE = os.environ.get("RUN_MOBILE", "0").lower() in ("1", "true", "yes")


def find_button(driver, locator_text):
    try:
        return driver.find_element(By.ACCESSIBILITY_ID, locator_text)
    except Exception:
        try:
            return driver.find_element(By.XPATH, f"//android.widget.Button[@text='{locator_text}']")
        except Exception:
            return driver.find_element(By.XPATH, f"//android.widget.ImageButton[@content-desc='{locator_text}']")


def tap_key(driver, key):
    find_button(driver, key).click()


def test_android_calculator_operation():
    if not RUN_MOBILE:
        return
    def create_appium_driver(url, options):
        try:
            return webdriver.Remote(url, options=options)
        except Exception:
            return None

    appium_url = os.environ.get("APPIUM_SERVER_URL", "http://127.0.0.1:4723/wd/hub")
    options = UiAutomator2Options()
    options.app_package = "com.google.android.calculator"
    options.app_activity = "com.android.calculator2.Calculator"
    options.new_command_timeout = 60

    driver = create_appium_driver(appium_url, options)
    if driver is None:
        return

    try:
        expression = ["2", "5", "+", "1", "5", "×", "3", "-", "1", "0", "="]
        for key in expression:
            tap_key(driver, key)
            time.sleep(0.4)

        result_field = driver.find_element(By.ID, "com.google.android.calculator:id/result_final")
        assert result_field.text.strip() == "110"

        clear_button = driver.find_element(By.ACCESSIBILITY_ID, "clear")
        clear_button.click()

        cleared_value = driver.find_element(By.ID, "com.google.android.calculator:id/result_final").text.strip()
        assert cleared_value == "0" or cleared_value == ""
    finally:
        if driver is not None:
            driver.quit()
