import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd



now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f'At time: {current_time} IST')



response = requests.get('https://in.tradingview.com/markets/stocks-india/market-movers-all-stocks/')
soup = BeautifulSoup(response.text, "html.parser")



# Find all stock names
all_stock_names = soup.find_all('span', class_='tickerCell-GrtoTeat')



# Find all stock descriptions
all_stock_descriptions = soup.find_all('sup', class_='apply-common-tooltip tickerDescription-GrtoTeat')


def Prices():
    table_columns = soup.find_all('tr', class_='row-RdUXZpkv listRow')
    prices = []
    for tr in table_columns:
        td_list = tr.find_all('td')  # Find all td elements within the tr
        if len(td_list) >= 3:  # Check if there are at least 3 td elements (0-based indexing)
            prices.append(td_list[1].text.strip())  # Append the text content of the 2nd td element (1st index)
    return prices

all_price = Prices()


def price_change():
    table_columns = soup.find_all('tr', class_='row-RdUXZpkv listRow')
    priceChanged = []
    for tr in table_columns:
        td_list = tr.find_all('td')
        if len(td_list) >= 3:
            priceChanged.append(td_list[2].text.strip())
    return priceChanged

change_in_price = price_change()


def volume_change():
    table_columns = soup.find_all('tr', class_='row-RdUXZpkv listRow')
    volumeChange=[]
    for tr in table_columns:
        td_list = tr.find_all('td')
        if len(td_list) >= 3:
            volumeChange.append(td_list[3].text.strip())
    return volumeChange
volume_changes=volume_change()


def rel_volume():
    table_columns=soup.find_all('tr', class_='row-RdUXZpkv listRow')
    rel_volume=[]
    for tr in table_columns:
        td_list=tr.find_all('td')
        if len(td_list) >=3:
            rel_volume.append(td_list[4].text.strip())
    return rel_volume
relative_volume=rel_volume()



def market_cap():
    table_columns = soup.find_all('tr', class_='row-RdUXZpkv listRow')
    market_cap=[]
    for tr in table_columns:
        td_list=tr.find_all('td')
        if len(td_list) >=3:
            market_cap.append(td_list[5].text.strip())
    return market_cap
market_capital=market_cap()


# print(f'Length of all_stock_names: {len(all_stock_names)}')
# print(f'Length of all_stock_descriptions: {len(all_stock_descriptions)}')
# print(f'Length of all_price: {len(all_price)}')
# print(f'Length of change_in_price: {len(change_in_price)}')



min_length = min(len(all_stock_names), len(all_stock_descriptions), len(all_price), len(change_in_price),len(volume_changes),len(relative_volume),len(market_capital))


# all_stock_names = all_stock_names[:min_length]
# all_stock_descriptions = all_stock_descriptions[:min_length]
# all_price = all_price[:min_length]
# change_in_price = change_in_price[:min_length]



# Collect data in lists
stock_data = []
for name, description, price, change,volume,relative_volume,mr_cap in zip(all_stock_names, all_stock_descriptions, all_price, change_in_price,volume_changes,relative_volume,market_capital):
    stock_data.append({
        'Stock Name': name.text.strip(),
        'Description': description.text.strip(),
        'Price': price,
        'Change': change,
        'Volume':volume,
        'Relative Volume':relative_volume,
        'Market Capital':mr_cap
    })




df = pd.DataFrame(stock_data)
excel_filename = 'stock_data.xlsx'
df.to_excel(excel_filename, index=False)

print(f'Data saved to {excel_filename}')
