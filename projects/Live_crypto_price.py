import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd

## to get the data in dictionary format
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'At time : {current_time} IST')

    response = requests.get('https://coinmarketcap.com/')
    text = response.text
    html_data = BeautifulSoup(text, 'html.parser')

    # Get the actual number of rows
    num_rows = len(html_data.find_all('tr'))

    headings = html_data.find_all('tr')[0]
    headings_list = []
    for x in headings:
        headings_list.append(x.text)
    headings_list = headings_list[:10]

    data = []

    for x in range(1, num_rows):  # Use the actual number of rows
        row = html_data.find_all('tr')[x]
        column_value = row.find_all('td')
        dict = {}

        for i in range(min(len(column_value), len(headings_list))):
            dict[headings_list[i]] = column_value[i].text
        data.append(dict)

    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    excel_filename = 'coinmarketcap_data.xlsx'
    df.to_excel(excel_filename, index=False)
    print(f'Data saved to {excel_filename}')

    # Wait for 60 seconds before scraping again
    time.sleep(60)



