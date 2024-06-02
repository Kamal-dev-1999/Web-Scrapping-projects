import requests
from bs4 import BeautifulSoup
import pandas as pd

# Collect doctor names and details from MedIndia
def get_doctor_details_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    all_doctor_divs = soup.find_all('div', class_='dirlist_box list-page')
    doctors = []
    
    for div in all_doctor_divs:
        h2_tag = div.find('h2')
        if h2_tag:
            a_tag = h2_tag.find('a')
            if a_tag:
                name = a_tag.text.strip()
                # Extract additional details
                specialization = div.find('small').text.strip() if div.find('small') else 'N/A'
                Address = div.find('span',class_="capitalize").text.strip() if div.find('span',class_="capitalize") else 'N/A'
                
                doctors.append({
                    'Doctor Name': name,
                    'Specialization': specialization,
                    'Address': Address
                })
    
    return doctors

base_url = "https://www.medindia.net/patients/doctor_search/doctors-mumbai.htm"
page_number = 1
all_doctors = []

while page_number <= 2:  # Modify this limit to scrape more pages
    # Modify the URL to include the page number
    if page_number == 1:
        url = base_url
    else:
        url = f"https://www.medindia.net/patients/doctor_search/doctors-mumbai-{page_number}.htm"
    
    doctors = get_doctor_details_from_page(url)
    
    if not doctors:
        break
    
    all_doctors.extend(doctors)
    page_number += 1

# Print all the collected doctor details
for doctor in all_doctors:
    print(doctor)

# Convert to DataFrame and save to Excel
df = pd.DataFrame(all_doctors)
excel_filename = 'doctor_data.xlsx'
df.to_excel(excel_filename, index=False)

print(f'Data saved to {excel_filename}')
