from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search(name):
    return name.replace(" ", "%20")

def scrape_amiami(name):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    base_url = "https://www.amiami.com/eng/search/list/?s_keywords="
    searchname = search(name)
    hashtable = []
    i = 1 # TRIED TO ADD SCRAPING MULTIPLE PAGES BUT COULD NOT WORK

    driver.get(base_url + searchname + "&pagecnt=" + str(i))
        
    try:
        # wait 10 seconds for elements to load
        images = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".newly-added-items__item__image_item"))
        )
        titles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "newly-added-items__item__name"))
        )
        prices = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "newly-added-items__item__price"))
        )

        for index, price_element in enumerate(prices):
            price = driver.execute_script("return arguments[0].childNodes[0].nodeValue;", price_element).strip() # get first instance of price only
            title = titles[index].text # get title
            child = images[index].find_element(By.TAG_NAME, "img")
            img = child.get_attribute("src") # get img
            hashtable.append({"productName": title, "productPrice": price, "productImg": img})

    except Exception as e:
        print(f"Error: {e}")
    
    driver.quit()
    return hashtable