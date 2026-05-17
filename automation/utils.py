import random
import string
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_unique_email(prefix: str = "user") -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{unique_id}@example.com"


def random_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def wait_for_element(driver, by: By, locator: str, timeout: int = 20):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))


def wait_for_clickable(driver, by: By, locator: str, timeout: int = 20):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))


def wait_for_text(driver, by: By, locator: str, text: str, timeout: int = 20):
    return WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element((by, locator), text))


def scroll_to_element(driver, element):
    """Scroll element into view"""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return element
