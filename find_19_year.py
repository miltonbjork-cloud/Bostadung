import requests
from bs4 import BeautifulSoup
import json
import os
from utils.paths import get_all_raw_list_files

def is_19_year_apartment(apartment_id):
    url = f"https://bostad.stockholm.se/bostad/{apartment_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return False
    html = response.text
    return "19 år" in html

def main():
    files = get_all_raw_list_files()
    found = []

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for apartment in data:
                apartment_id = apartment[0]  # ID ligger i index 0
                if is_19_year_apartment(apartment_id):
                    found.append(f"https://bostad.stockholm.se/bostad/{apartment_id}")
    
    print("Hittade 19-årsbostäder:")
    for link in found:
        print(link)

if __name__ == "__main__":
    main()
