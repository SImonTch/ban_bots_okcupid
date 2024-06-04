import json
import random
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


# Load cookies from JSON file
with open('cookies.json', 'r') as file:
    cookies = json.load(file)

# Create a new instance of the Firefox webdriver
browser = webdriver.Firefox()  # Make sure you have geckodriver installed and in PATH

# Navigate to the OkCupid login page
browser.get('https://www.okcupid.com/login')

# Add cookies to the webdriver
for cookie in cookies:
    browser.add_cookie({
        'name': cookie['name'],
        'value': cookie['value'],
        'domain': cookie['domain'],
        'path': cookie['path'],
        'secure': cookie['secure'],
        'httpOnly': cookie['httpOnly']
    })

# Refresh the page to apply the cookies
browser.refresh()

# Wait for the page to load completely
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

def click_button(xpath, timeout=20, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            # Wait for the element to be present in the DOM
            element = WebDriverWait(browser, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

            # Wait for the element to be clickable (optional)
            WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Introduce a random delay
            time.sleep(random.uniform(1, 3))
            # Click on the button
            element.click()
            return

        except (StaleElementReferenceException, TimeoutException) as e:
            retries += 1
            print(f"Exception occurred: {e.__class__.__name__}. Retrying ({retries}/{max_retries})...")

    raise Exception(f"Failed to click the button after {max_retries} retries.")


# Click on the first button
click_button('//*[@id="stack-menu-item-PENPAL"]')


# Loop for clicking button3 and button4
num_iterations = 10  # Specify the number of times to loop
for i in range(num_iterations):
    print(f"Iteration {i+1}/{num_iterations}")

    # Click on the second button
    click_button("/html/body/div[1]/main/div/div[4]/div/div[2]/div[1]/div[1]/div[2]/div[2]/button")

    # Click on the third button
    click_button("/html/body/div[3]/div[1]/div/div/div/div[5]/button")

    # Click on the fourth button
    click_button("/html/body/div[3]/div[1]/div/div/div/div/button")

    # Introduce a random delay between iterations
    time.sleep(random.uniform(2, 5))

# Perform further actions on the page as needed

# Close the webdriver when done
browser.quit()