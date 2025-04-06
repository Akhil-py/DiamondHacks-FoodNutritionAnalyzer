#product name, brand, 100 products per search
#product information + important information to akhil

# scraper-python.py
# To run this script, paste `python scraper-python.py` in the terminal

import requests
from bs4 import BeautifulSoup
import pandas as pd

from scrapingbee import ScrapingBeeClient

def scrape(product, brand, found):
    api_key ='ROEG0293KVWCCSIRM3KYDSUTXPY95BVTDR2NSAIDN3JRXIILA4S0IDFTPXNTKGGWDMUFTRWV1LXDDYXI'
    
    # Construct search query

    query = f"{product}+{brand}".replace(" ", "+")
    url = f"https://www.amazon.com/s?k={query}"

    payload = {
        'api_key': api_key,
        'url': url,
        'render_js': 'false'  # Set to true if JS rendering is needed
    }

    #http request
    response = requests.get('https://app.scrapingbee.com/api/v1/', params=payload)
    # print(f"Status Code: {response.status_code}")
    # print(response.content)

    product_list = []

    if response.status_code != 200:
        print("Failed to retrieve search page:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a', attrs = {'class': 'a-link-normal s-no-outline'})

    if not links:
        print("No links found on Amazon search page")
        return []
    
    if found: 
        # print("https://www.amazon.com" + links[0].get('href'))
        return "https://www.amazon.com" + links[0].get('href')
    else: 
        product_list = ["https://www.amazon.com" + link.get('href') for link in links[:20] if link.get('href')]
    
    # print(f"Found {len(product_list)} product links")

    product_data = []

    for product in product_list:
        product_payload = {
            'api_key': api_key,
            'url': product,
            'render_js': 'false'  # Set to true if JS rendering is needed
        }

        product_page = requests.get('https://app.scrapingbee.com/api/v1/', params=product_payload)
        # print(f"[{product}] Status Code: {product_page.status_code}")

        new_soup = BeautifulSoup(product_page.content, 'html.parser')

        title_tag = new_soup.find('span', id='productTitle')
        brand_tag = new_soup.find('a', id='bylineInfo')
        info_tag = new_soup.find('div', id='productDescription')
        ingredient_tag = new_soup.find(string=lambda t: "ingredients" in t.lower())

        product_info = {
            "Title": title_tag.text.strip() if title_tag else "N/A",
            "Brand": brand_tag.text.strip() if brand_tag else "N/A",
            "Description": info_tag.text.strip() if info_tag else "N/A",
            "Ingredients": ingredient_tag.text.strip() if ingredient_tag else "N/A",
            "URL": product
        }

        product_data.append(product_info)

    # print(product_data)

    return product_data
    
if __name__ == '__main__':
    scrape("chips", "lays", True)
