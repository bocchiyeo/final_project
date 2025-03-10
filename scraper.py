import requests
from bs4 import BeautifulSoup

def search(name):
    return name.replace(" ", "%20")  # Return the modified string

base_url = "https://www.amiami.com/eng/search/list/?s_keywords="
name = "The Apothecary Diaries"
searchname = search(name)

i = 1  # Page counter

while True:
    url = f"{base_url}{searchname}&pagecnt={str(i)}"  # Format URL correctly
    response = requests.get(url)
    print(BeautifulSoup(response.text, "html.parser")) # FIND A WAY TO BYPASS CLOUDFLARE
    if response.status_code != 200:  # Check for request failure
        print(f"Failed to retrieve page {i}")
        break
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    items = soup.find_all("p", class_="newly-added-items__item__image_item")
    
    if not items:  # If no items found, stop searching
        print(f"No more items found on page {i}. Stopping search.")
        break

    # If items exist, process them
    print(f"Page {i}: Found {len(items)} items.")
    
    i += 1  # Move to the next page

