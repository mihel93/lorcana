import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

def get_table_rows(table_url, timeout=10, delay_after_cookies=2, min_wait=2, max_wait=15):
    # Set up custom headers to simulate a regular browser request
    custom_headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        "accept": "*/*",
        "accept-language": "bg-BG,bg;q=0.9,en;q=0.8,nl;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd"
    }

    # Initialize Chrome WebDriver with options
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # Modify request headers by adding custom headers
    driver.request_interceptor = lambda request: request.headers.update(custom_headers)

    # Open the URL with modified headers
    driver.get(table_url)

    # Initialize an empty list to store each row of table data
    rows = []

    # Set up explicit wait for dynamically loaded elements
    wait = WebDriverWait(driver, timeout)

    # Locate and click the "Accept Cookies" button if present
    cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="allowAllButton"]')))
    ActionChains(driver).move_to_element(cookies_button).click().perform()

    # Introduce a short wait to ensure all elements load after accepting cookies
    time.sleep(delay_after_cookies)

    # Locate and click the "Refresh" button to load table data
    refresh_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-sm btn-primary data-tables-refresh-button"]'))
    )
    ActionChains(driver).move_to_element(refresh_button).click().perform()

    # Wait until "Next" button becomes clickable, indicating that pagination is available
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="paginate_button next"]')))

    # Loop through pages by repeatedly clicking the "Next" button until no more pages are left
    while True:
        # Find and retrieve the table element that contains the rows
        table = wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody')))

        # Use BeautifulSoup to parse the HTML of the table for row extraction
        soup = bs(table.get_attribute('outerHTML'), 'html.parser')

        # Extract and store each row within the table
        table_rows = soup.find_all('tr')
        for row in table_rows:
            rows.append(row)

        # Introduce a randomized wait time before clicking "Next" to reduce the risk of detection
        random_wait = random.uniform(min_wait, max_wait)
        time.sleep(random_wait)

        # Attempt to locate and click the "Next" button to move to the next page
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="paginate_button next"]')))
            ActionChains(driver).move_to_element(next_button).click().perform()

            # Re-confirm "Next" button is available for the next iteration
            wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="paginate_button next"]')))

        except:
            # If "Next" button is not found/clickable, we assume we've reached the last page
            print("Reached the last page.")
            break

    # Close the WebDriver session to free resources
    driver.quit()

    # Return the collected rows for further processing
    return rows


