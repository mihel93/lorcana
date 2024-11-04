# Lorcana Tournament Scraper

This Python script scrapes tournament event data from a webpage for Lorcana Tournaments, storing it in a CSV file (`lorcana_events.csv`). By running this script, new event data is appended to the CSV only if it doesn't already exist, helping to avoid duplicate entries.

## Requirements

- **Python 3.x**
- **Pandas**: `pip install pandas`
- **BeautifulSoup**: `pip install beautifulsoup4`
- **Selenium**: `pip install selenium`
- Chrome WebDriver (compatible with your version of Chrome)

## Usage
1. Set Up Chrome WebDriver:

- Ensure ChromeDriver is installed and added to your PATH or specify its location in the script.
- Download ChromeDriver from here if needed.

2. Run the script:

- Execute **_lorcana_scraper.py_**  to scrape data from the Lorcana tournament table and save it to the CSV file.


## Functions

### _**get_table_rows(table_url)**_

This function takes the URL of a tournament table and returns a list of rows containing tournament event data.

#### Features
- Automated Table Row Extraction: Collects all table rows of tournament data from each page.
- Pagination Handling: Iterates through pages by clicking the "Next" button until reaching the last page.
- Customizable Delays: Uses random delays between page navigations to simulate human browsing.
- Cookie Acceptance: Automatically clicks the "Accept Cookies" button, simplifying navigation.

#### Run the Script:

- Import the get_table_rows function and pass the desired table URL.

- Configure Custom Delays and Timeout:

- Adjust timeout, delay_after_cookies, min_wait, and max_wait as needed for your target site.

#### Notes
Ensure compliance with the website's terms of service before scraping.
Delays are added to prevent excessive server load and simulate real user behavior.

### _**get_event_location(event_link)**_

- Given a link to an event, this function scrapes the event's location and returns:

    - location: Name of the location
    - location_link: Link to the event location details
    
#### Features

- Sets custom request headers to mimic a browser session.
- Accepts cookies if prompted.
- Clicks on a tooltip-trigger link to reveal location data.
- Extracts the location name and link from the tooltip using BeautifulSoup.
- Error Handling
    - If the location data cannot be extracted (e.g., due to missing elements), the function returns (None, None) and closes the browser session to free resources.

#### Run the Script:

- Ensure that you have the Chrome WebDriver installed and that it's compatible with your version of Chrome. You can download it from here.
- Import the get_location function and pass the event link URL.


## Key Variables

- table_url: The URL of the Lorcana tournament table page.
- rows: A list of HTML rows representing individual events, scraped from the table.

## CSV Fields

_Each row in lorcana_events.csv contains:_

- date: Event date
- name: Event name
- event: Link to the event page
- location: Event location name
- location_link: Link to location details
- organizer: Name of event organizer
- status: Event status (upcoming, ongoing, completed)
- reg_type: Registration type (free, paid)
- entry_fee: Cost to enter the event
- players: Number of players enrolled
- tags: Event tags (online, in-person, etc.)

## Note

The script introduces random wait times between event processing cycles to mimic realistic browsing behavior.

## License

This project is open-source and free to use.



This `README.md` provides an overview, requirements, setup instructions, function explanations, and fie
