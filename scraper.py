import requests
import pandas as pd
from bs4 import BeautifulSoup

start_url = "https://en.wikipedia.org/w/index.php?title=List_of_brightest_stars_and_other_record_stars&oldid=1076654151"

def scrape():
    response = requests.get(start_url)
    if response.status_code == 200: #Basically if the request is successful. Yeah.
        soup = BeautifulSoup(response.content, "html.parser")
        bright_star_table = soup.find("table", class_="wikitable")
        table_rows = bright_star_table.find_all('tr')

        scraped_data = []

        for row in table_rows:
            table_cols = row.find_all('td')
            temp_list = []

            for col_data in table_cols:
                data = col_data.text.strip()
                temp_list.append(data)
                scraped_data.append(temp_list)

        return scraped_data
    else:
        print("Couldn't get the webpage. Sorry.")
        return None

scraped_data = scrape()

if scraped_data:
    stars_data = []
    for data in scraped_data:
        Star_names = data[1]
        Distance = data[3]
        Mass = data[5]
        Radius = data[6]
        Lum = data[7]
        required_data = [Star_names, Distance, Mass, Radius, Lum]
        stars_data.append(required_data)

    headers = ['Star_name', 'Distance', 'Mass', 'Radius', 'Luminosity']

    star_df = pd.DataFrame(stars_data, columns=headers)
    star_df.to_csv('scraped_data.csv', index=True, index_label="id")
    print("Data saved successfully to scraped_data.csv :)")
