from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

# Path to the ChromeDriver
chrome_driver_path = r"C:\Users\Amir\Downloads\chromedriver-win32\chromedriver.exe"

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Navigate to Google login page
    driver.get("https://accounts.google.com/ServiceLogin")

    # Maximize the browser window
    driver.maximize_window()

    # Wait for the email input field to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )

    # Enter email address
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys("amirbehvandi747@gmail.com")  # Replace with your email
    email_input.send_keys(Keys.RETURN)

    # Wait for the password input field to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    # Enter password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("Eddy@747Sahar")  # Replace with your password
    password_input.send_keys(Keys.RETURN)

    # Wait for the page to load after login
    time.sleep(5)  # Adjust the sleep time if needed to allow login to complete

    # Check for any additional Google security prompts or two-factor authentication here if applicable

    # Now that you're logged in, go to the target chat page
    driver.get("https://chatgpt.com/c/6797543d-84dc-8000-8832-1d59b535b651")  # Replace with the actual URL

    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Check if the element is inside an iframe
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        print("Switched to iframe")
    except NoSuchElementException:
        print("No iframe found, proceeding with the main document.")

    # Wait for the input field to appear
    try:
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        print("Input field located!")

        # Interact with the input field
        chat_input.send_keys("Hello, world!")
        chat_input.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Input field not found within the specified time.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Debug: Output the page source if there's an issue
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
        print("Page source saved to 'page_source.html' for debugging.")

    # Close the browser
    driver.quit()
