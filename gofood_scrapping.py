import __main__
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

driver = webdriver.Chrome()

location_store = []
store_name = []
category = []
rating = []
rating_count = []
recent_review = []
path = []
latitude = []
longitude = []

def merchant_path(json):
    f = open(json)
    data = json.load(f)
    for outlet in data.get("props", {}).get("pageProps", {}).get("outlets", []):
        latitude.append(outlet.get("core").get("location").get("latitude"))
        longitude.append(outlet.get("core").get("location").get("longitude"))
        path.append("https://gofood.co.id" + outlet.get("path", ""))

def gofood_scrapping(path,review_count=5):
    for url in path: 
        driver.get(url)
        # body = driver.find_element(By.TAG_NAME, 'body')
        # for _ in range(5):
        #     body.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(2)
        # for _ in range(5):
        #     body.send_keys(Keys.PAGE_UP)
        #     time.sleep(2)    

        time.sleep(4)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        try:
            store_name.append(soup.find("h1",{"class":"overflow-x-hidden overflow-ellipsis max-h-[6rem] text-gf-content-primary gf-heading-xl md:max-h-[4rem] md:gf-heading-2xl"}).get_text())
        except AttributeError:
            store_name.append("none")
        try:
            rating.append(soup.find("p", {"class": "gf-label-s md:gf-label-l"}).get_text())
        except AttributeError:
            rating.append("none")
        try:
            category.append(soup.find("p",{"class":"text-gf-content-secondary line-clamp-1 gf-body-s md:gf-body-m lg:gf-body-l"}).get_text())
        except AttributeError:
            category.append("none")
            
        time.sleep(4)

        try:
            element = driver.find_element(By.CSS_SELECTOR, "div.shrink-0.grow-0.text-gf-content-primary.gf-body-s.md\\:gf-body-m a.text-gf-content-brand.gf-label-s.cursor-pointer.md\\:gf-label-m")
            element.click()
            time.sleep(4)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            try:
                for page in soup.find_all("div", {"class": "flex flex-col space-y-10"}):
                    stars = page.find_all("span", {"class": "ml-1 inline-block"})
                    comments = page.find_all("p", {"class": "break-words gf-body-m"})

                    temp_reviews = []
                    for star, comment in zip(stars, comments):
                        if len(temp_reviews) < review_count: 
                            temp_reviews.append(f"Star {star.text} {comment.text}")
                        else:
                            break 
            
                    if temp_reviews:
                        recent_review.append("\n".join(temp_reviews))
                    else:    
                        recent_review.append("none")
            except AttributeError:
                recent_review.append("none")
            
            time.sleep(4)
            try:
                rating_count.append(soup.find("div",{"class":"text-gf-content-muted gf-body-s md:gf-body-m"}).get_text())
            except AttributeError:
                rating_count.append("none")
        except Exception as e:
            print("Error clicking the element:", e)

        driver.back()
        time.sleep(4)

        try:
            element = driver.find_element(By.CSS_SELECTOR, ".pl-2 .relative .cursor-pointer")
            element.click()
            time.sleep(4)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            try:
                time.sleep(4)
                location_store.append(soup.find("div",{"class":"text-gf-content-muted gf-body-s"}).get_text())
            except AttributeError:
                location_store.append("none")
                print("Error clicking the element:", e)
        except Exception as e:
            print("Error clicking the element:", e)

                
        time.sleep(4)

df = pd.DataFrame()
df["merchant"] = store_name
df["category"] = category
df["rating"] = rating
df["rating_count"] = rating_count
df["recent_review"] = recent_review
df["location"] = location_store
df["longitude"] = longitude
df["latitude"] = latitude

df.to_excel("gofood.xlsx", index=False)

if __name__ == __main__:
    merchant_path("outlet.json")
    gofood_scrapping(path,review_count=5)
    driver.quit()