from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

def search(name):
    """Format search term for AmiAmi URL."""
    return name.replace(" ", "%20")

def scrape_amiami(name, pages=1):
    """Scrape AmiAmi for product details.

    Args:
        name (str): The product search query.
        pages (int): Number of pages to scrape.

    Returns:
        list: A list of dictionaries containing product details.
    """
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    base_url = "https://www.amiami.com/eng/search/list/?s_keywords="
    searchname = search(name)
    hashtable = []

    try:
        # loop through pages
        for i in range(1, pages + 1): 
            driver.get(base_url + searchname + "&pagecnt=" + str(i))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait 20s for elements to load
            products = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".newly-added-items__item.nomore"))
            )

            # extract product details from each product container
            for product in products:
                try:
                    # check for the presence of each element before extracting details
                    title_element = product.find_element(By.CLASS_NAME, "newly-added-items__item__name")
                    price_element = product.find_element(By.CLASS_NAME, "newly-added-items__item__price")
                    img_element = product.find_element(By.CSS_SELECTOR, ".newly-added-items__item__image_item img")
                    link_element = product.find_element(By.XPATH, ".//a[contains(@href, '/eng/detail/?gcode=GOODS-')]")

                    # extract details if all elements are present
                    title = title_element.text
                    price = price_element.text.strip().split()[0]
                    img = img_element.get_attribute("src")
                    link = link_element.get_attribute("href")

                    # append details to hashtable
                    hashtable.append({
                        "productName": title, 
                        "productPrice": price, 
                        "productImg": img, 
                        "productLink": link, 
                        "source": "AmiAmi"
                    })
                except Exception as e:
                    continue

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return hashtable
