print("Importing general tools...")
import pickle
import time
import random
import re

print("Importing scraping tools...")
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

# Create Selenium webdriver with Chrome Headless
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)



def scrape_reviews(url):
    # Step 1: get page source
    page = driver.page_source
    soup = BeautifulSoup(page, features="lxml")
    
    # Step 2: scrape reviews and put in list
    reviews_raw = soup.find_all('div', {'class' : re.compile("(text show-more__control|text show-more__control clickable)")})
    reviews_list = list(reviews_raw)  
    print(f"Scraped {len(reviews_list)} reviews.")

    return reviews_list

# remove HTML tags
TAG_RE = re.compile(r'(<[^>]+>|\n)')
def remove_tags(text):
    return TAG_RE.sub("", text)

# Program Start
print("Start Time: ", time.strftime("%m/%d/%Y, %H:%M:%S"))

# Open relevant files
print("Opening pickles...")

# with open("clean_dict.pickle", "rb") as read_file:
#     clean_dict = pickle.load(read_file)

with open("all_keys.pickle", "rb") as read_file:
    all_keys = pickle.load(read_file)

# Scrape
print("Calculating...")
simple_scrape_dict = {}
# remaining_keys = [i for i in all_keys if i not in list(clean_dict.keys())]
remaining_keys = all_keys
failed_keys = []
count = 0
for key in remaining_keys:
    url = key[1]+"reviews?ref_=tt_ql_3"
    print(f"Fetching reviews of {key[0]}...")
    driver.get(url)
    try:
        val_raw = scrape_reviews(url)
    except:
        time.sleep(10)
        try:
            val_raw = scrape_reviews(url)
        except:
            failed_keys.append(key)
            continue
    val_clean = []
    for review in val_raw:
        review_clean = remove_tags(str(review))
        val_clean.append(review_clean)
    simple_scrape_dict[key] = val_clean
    count += 1
    print(key)
    if count%10 == 0:
        print("**************")
        print(f"Successfully scraped {count} of {len(remaining_keys)} urls.")
        current_time = time.strftime("%m/%d/%Y, %H:%M:%S")
        print(f"Current Time = {current_time}.")
        print("**************")
        with open("simple_scrape_dict.pickle", "wb") as to_write:
            pickle.dump(simple_scrape_dict, to_write)
        with open("failed_keys.pickle","wb") as to_write:
            pickle.dump(failed_keys, to_write)
