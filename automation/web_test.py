import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from automation.utils import generate_unique_email, random_password, wait_for_clickable, wait_for_element, scroll_to_element


def test_automation_exercise_complete_flow():
    email = generate_unique_email("automation")
    password = random_password(10)
    name = "Test User"

    # Configure Chrome options to handle ads better
    chrome_options = Options()
    chrome_options.add_argument('--disable-ads')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images to load faster
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        driver.get("https://automationexercise.com/")
        assert "Automation Exercise" in driver.title

        login_link = wait_for_clickable(driver, By.LINK_TEXT, "Signup / Login")
        login_link.click()

        name_input = wait_for_element(driver, By.NAME, "name")
        email_input = wait_for_element(driver, By.XPATH, "//input[@data-qa='signup-email']")
        name_input.send_keys(name)
        email_input.send_keys(email)

        signup_button = wait_for_clickable(driver, By.XPATH, "//button[@data-qa='signup-button']")
        signup_button.click()

        password_input = wait_for_element(driver, By.ID, "password")
        password_input.send_keys(password)
        driver.find_element(By.ID, "first_name").send_keys("Test")
        driver.find_element(By.ID, "last_name").send_keys("User")
        driver.find_element(By.ID, "address1").send_keys("123 Test Street")
        driver.find_element(By.ID, "country").send_keys("Canada")
        driver.find_element(By.ID, "state").send_keys("Ontario")
        driver.find_element(By.ID, "city").send_keys("Toronto")
        driver.find_element(By.ID, "zipcode").send_keys("M5H 2N2")
        driver.find_element(By.ID, "mobile_number").send_keys("+14165551234")

        create_account_button = wait_for_element(driver, By.XPATH, "//button[@data-qa='create-account']")
        # Scroll to button and close any overlays
        scroll_to_element(driver, create_account_button)
        time.sleep(1)
        # Try to close any ad iframes by scrolling
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        # Click with JavaScript if regular click fails
        try:
            create_account_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", create_account_button)

        account_created_message = wait_for_element(
            driver,
            By.XPATH,
            "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'ACCOUNT CREATED')]",
        )
        assert account_created_message.is_displayed()

        continue_button = wait_for_clickable(driver, By.XPATH, "//a[contains(normalize-space(.), 'Continue')]")
        continue_button.click()
        time.sleep(2)

        logged_in_text = wait_for_element(driver, By.XPATH, "//a[contains(text(),'Logged in as')]" )
        assert name in logged_in_text.text

        # Products link might not be immediately available, try multiple selectors
        products_link = None
        try:
            products_link = wait_for_clickable(driver, By.LINK_TEXT, "Products", timeout=10)
        except Exception:
            # Try alternative selector
            products_link = wait_for_clickable(driver, By.XPATH, "//a[contains(text(), 'Products') or contains(@href, 'products')]", timeout=10)
        scroll_to_element(driver, products_link)
        products_link.click()

        first_product = wait_for_clickable(driver, By.XPATH, "(//div[@class='product-overlay']/div/a)[1]")
        first_product.click()

        add_to_cart = wait_for_clickable(driver, By.XPATH, "//button[contains(text(),'Add to cart')]")
        add_to_cart.click()

        time.sleep(3)
        continue_shopping = wait_for_clickable(driver, By.XPATH, "//button[contains(text(),'Continue Shopping') or contains(@class, 'continue')]" )
        continue_shopping.click()

        cart_button = wait_for_clickable(driver, By.XPATH, "//a[contains(@href,'/view_cart')]" )
        cart_button.click()

        subtotal = wait_for_element(driver, By.XPATH, "//td[contains(text(),'Subtotal') or contains(text(),'Price')]" )
        assert subtotal is not None

        driver.get("https://automationexercise.com/delete_account")
        delete_message = wait_for_element(driver, By.XPATH, "//b[contains(text(),'Account Deleted')]" )
        assert delete_message.is_displayed()
    finally:
        driver.quit()
