from google import genai

client = genai.Client(api_key="AIzaSyBWkxvfe9n3bWTRJ_O4gRhIpPpv7SaQ3pU")

query = "toothpaste"

instructions1 = "Analyze the description of the product and provide a ranking \
            on a scale of 1 to 5 based on its healthiness and nutritional \
            value in comparison to other similar products in the same \
            industry/type. Give me this ranking in the begining of the message \
            in the format: 'RANK=x' where x is the rank. Provide a brief \
            explanation of the ranking and suggest any alternative products that \
            could be purchased as a healthier alternative. Also, provide a list \
            of any potential allergens or harmful ingredients present in the product."

instructions2 = "Find the most healthy brand options or sustainably sourced \
        brands for the category of ", query, " and provide a list of the top 5 brands. \
        Provide a brief explanation of why these brands are considered healthier or more \
        sustainable. Also, include any certifications or labels that these brands have \
        received for their healthiness or sustainability."

description = "" # This discripption will come from the web scraping part of the code
description = "Colgate Cavity Protection Toothpaste Great Regular Flavor 1 oz (Pack of 12) - Brand	Colgate Flavor	Regular Age Range (Description)	Adult Item Form	Paste Material Type Free	[INFERRED: Sodium Monofluorophosphate, Gluten, Methylisothiazolinone, and Triclosan Free] About this item Helps protect teeth against cavities Cleans teeth thoroughly Freshens breath Country of origin is United States. Product details Is Discontinued By Manufacturer  :  No Product Dimensions :  3.94 x 1.5 x 0.79 inches; 1.02 Pounds Item model number  :  1003500051 Date First Available  :  July 31, 2013 Manufacturer  :  Colgate ASIN  :  B00FD89UIW"

analysis = client.models.generate_content(
    model="gemini-2.0-flash", contents=instructions2
)

list = client.models.generate_content(
    model="gemini-2.0-flash", contents="Give me an array of the top 5 brands for the category of " + query + " based on its healthiness and sustainability. Don't include any other information, just the brand names in a list format: [product 1, product 2, product 3, product 4, product 5]."
)

#rank = (analysis.text.split("RANK=")[1].split("\n")[0].strip())
#print(f"Healthiness Rank: {rank}")
#print(analysis.text)
print(list.text)