#product name, brand, 100 products per search
#product information + important information to akhil

# scraper-python.py
# To run this script, paste `python scraper-python.py` in the terminal

import requests
from bs4 import BeautifulSoup
import pandas as pd
#from os import sched_setparam

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


    # print(links)
    # print(found)

    if not links:
        # print("No links found on Amazon search page")
        return "No links found on Amazon search page"



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


def search(search_term):
    nutri_score_values = {
        'a': 5,
        'b': 4,
        'c': 3,
        'd': 2,
        'e': 1
    }
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": search_term,
        "json": "true"
    }
    response = requests.get(url, params=params)

    products_list = []

    if response.status_code == 200:
        data = response.json()
        if 'products' not in data:
          return
        if len(data["products"]) > 0:
            for product in data["products"]:
                nutrition_grade = product.get("nutrition_grades")
                if not nutrition_grade:
                    continue
                grade = nutri_score_values.get(nutrition_grade)
                if grade:
                    product_info = {
                        "product_name": product.get("product_name"),
                        "brand": product.get("brands"),
                        "nutrition_grade": grade
                    }
                    products_list.append(product_info)
        else:
            print("No products found for your search term.")
    else:
        print(f"Error: {response.status_code}")
    # Sort the products by nutrition grade (from 5 to 1)
    sorted_products = sorted(products_list, key=lambda x: x["nutrition_grade"], reverse=True)
    top_20_products = sorted_products[:20]
    # Display sorted products
    retList = []
    if top_20_products:
        # print("Sorted Products:")
        for product in top_20_products:
          if(scrape(product['product_name'], product['brand'], True) != "No links found on Amazon search page"):
            retVals ={
                "product_name": product['product_name'],
                "brand": product['brand'],
                "nutrition_grade": product['nutrition_grade'],
                "amazon_link": scrape(product['product_name'], product['brand'], True)
            }
            retList.append(retVals)
            # print(f"Product Name: {product['product_name']}")
            # print(f"Brand: {product['brand']}")
            # print(f"Nutrition Grade: {product['nutrition_grade']}")
            # scrape(product['product_name'], product['brand'], True)
          # print(f"Product Name: {product['product_name']}")
          # print(f"Brand: {product['brand']}")
          # print(f"Nutrition Grade: {product['nutrition_grade']}")
          # scrape(product['product_name'], product['brand'], True)
          # print()
    else:

        print("No products found for your search term.")
        scrape(search_term, "none", False)
    return retList

search_term = input("What are you looking for: ")
search(search_term)
