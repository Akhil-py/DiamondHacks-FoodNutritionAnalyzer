import requests

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
    if top_20_products:
        print("Sorted Products:")
        for product in top_20_products:
            print(f"Product Name: {product['product_name']}")
            print(f"Brand: {product['brand']}")
            print(f"Nutrition Grade: {product['nutrition_grade']}")
            scrape(product['product_name'], product['brand'], True)
            print()
    else:
        
        print("No products found for your search term.")
        scrape(search_term, "none", False)
        
search_term = input("What are you looking for: ")
search(search_term)
