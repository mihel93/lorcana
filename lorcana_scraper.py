import pandas as pd
import random
import time
from get_location import get_event_location
from get_table import get_table_rows

# URL of the page to scrape tournament data for Lorcana
table_url = "https://melee.gg/Tournament/Index?ordering=StartDate&filters=Lorcana&mode=Table"

# Retrieve rows from the tournament table using the 'get_table_rows' function
rows = get_table_rows(table_url)

# Iterate over each event row to extract and save event details
for row in rows:

    # Load existing events from CSV to avoid duplicating entries
    events_df = pd.read_csv('lorcana_events.csv')

    # Get event link from the 'name-column' and construct full URL
    name_column = row.find('td', class_="name-column")
    event_link = f"https://melee.gg{name_column.find('a')['href']}"

    # Skip this event if it already exists in the CSV
    if event_link in events_df['event'].values:
        pass  # Event already exists, skip to the next

    else:
        # If event is new, retrieve event location and link using 'get_event_location' function
        location, location_link = get_event_location(event_link)

        # Extract event details (date, name, organizer, etc.) from table columns
        date = row.find('td', class_="startDate-column").text.strip()
        name = name_column.find('a').text.strip()
        organizer_column = row.find('td', class_="organizationName-column")
        organizer = organizer_column.find('a').text.strip()
        status = row.find('td', class_="status-column").text.strip()
        reg_type = row.find('td', class_="registrationType-column").text.strip()
        entry_fee = row.find('td', class_="entryFeeString-column").text.strip()
        players = int(row.find('td', class_="enrolledPlayerCount-column").text.strip())

        # Collect event tags (e.g., online, in-person) from 'tournament-results-table-tag' elements
        tags = [tag.text.strip() for tag in row.find_all('span', class_="tournament-results-table-tag")]

        # Organize extracted data into a dictionary for the new event
        new_event = {
            'date': [date],
            'name': [name],
            'event': [event_link],
            'location': [location],
            'location_link': [location_link],
            'organizer': [organizer],
            'status': [status],
            'reg_type': [reg_type],
            'entry_fee': [entry_fee],
            'players': [players],
            'tags': [tags]
        }

        # Convert the dictionary to a DataFrame and append to existing events
        event_df = pd.DataFrame(new_event)
        events_df = pd.concat([events_df, event_df], ignore_index=True)

        # Save updated DataFrame back to the CSV
        events_df.to_csv('lorcana_events.csv', index=False)

        # Wait for a random time before processing the next event
        random.seed(565856215)
        random_wait = random.uniform(2, 15)
        time.sleep(random_wait)
