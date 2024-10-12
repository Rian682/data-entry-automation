import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


########## Part 1: BeautifulSoup ##########

site = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=New-Delhi&BudgetMax=10-Lacs"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/129.0.6668.100 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
    "DNT": "1"
}

response = requests.get(site, headers)
site_html = response.text
soup = BeautifulSoup(site_html, "html.parser")


j_son = []
description_list = []
price_list = []
link_list = []
rooms_list = []


all_prices = soup.find_all("div", class_="mb-srp__card__price--amount")
all_descriptions = soup.find_all("p")
links_rooms = soup.find_all("script", {"type": "application/ld+json"})


for d in all_descriptions:
    description_list.append(d.text)

for p in all_prices:
    price_list.append(p.text)

for n in links_rooms:
    ans = (json.loads(n.text))
    j_son.append(ans)

for L in j_son:
    if '@id' and 'numberOfRooms' in L:
        link_list.append(L['@id'])
        rooms_list.append(L['numberOfRooms'])


############# Part 2: Selenium ##############

driver_path = r"D:\Development\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

for i in range(len(rooms_list)):

    # you can create your own Google form with a description box, number of rooms, price and link
    # and copy the form url below to get the responses.
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSftRMLN6GcKww3Qpw6_dA-d0kkVd2Heob-eg-yz4r-gtlEkxA/viewform?usp=sf_link")
    time.sleep(5)

    description_box = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    description_box.send_keys(description_list[i])

    num_of_rooms = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    num_of_rooms.send_keys(rooms_list[i])

    rent = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    rent.send_keys(price_list[i])

    property_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link.send_keys(link_list[i])

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()

    time.sleep(5)


input("Press Enter to close...")
driver.quit()

