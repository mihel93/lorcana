from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import random
import time

def get_event_location(event_link, timeout=10, min_wait=2, max_wait=5):
    # Set custom headers to mimic a real browser request
    custom_headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        "accept": "*/*",
        "accept-language": "bg-BG,bg;q=0.9,en;q=0.8,nl;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd"
    }

    # Initialize Chrome WebDriver with specified options
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # Modify request headers
    driver.request_interceptor = lambda request: request.headers.update(custom_headers)

    # Open the event link URL, appending "#" to avoid caching issues
    driver.get(event_link + '#')

    # Set up an explicit wait for dynamic elements
    wait = WebDriverWait(driver, timeout)

    # Locate and click "Accept Cookies" button if present
    cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="allowAllButton"]')))
    ActionChains(driver).move_to_element(cookies_button).click().perform()

    # Introduce a random wait to simulate realistic browsing
    random.seed(565856215)
    random_wait = random.uniform(min_wait, max_wait)
    time.sleep(random_wait)

    try:
        # Locate and click on the link that triggers the tooltip with event location
        popover_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-toggle="hovercard"]')))
        ActionChains(driver).move_to_element(popover_link).click().perform()

        # Wait for the tooltip containing location info to appear
        tooltip = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="tooltip"]')))

        # Parse the tooltip HTML content with BeautifulSoup
        soup = bs(tooltip.get_attribute('outerHTML'), 'html.parser')

        # Extract location name and URL from the tooltip content
        location = soup.find('a', href=True).get_text(strip=True)
        location_link = soup.find('a', href=True)['href']

    except Exception:
        # Close driver in case of an error and return None values for location details
        driver.quit()
        return None, None

    # Close the driver and return extracted location details
    driver.quit()
    return location, location_link
