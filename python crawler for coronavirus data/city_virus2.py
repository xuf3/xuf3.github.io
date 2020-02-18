from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import sqlite3
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
#put the path to your own chromedriver
browser = webdriver.Chrome("/Users/FengyuXu/Desktop/web_crawler/twitter_crawler/chromedriver")

now = str(datetime.now())

placeName = {}
with open("name.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        placeItem = line.replace("\n", "").split(",")
        placeName[placeItem[0]] = placeItem[1]

cityName = {}
with open("CityName.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    for line in lines:
        cityItem = line.replace("\n", "").split(",")
        cityName[cityItem[1]] = cityItem[3]

url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"

browser.get(url)

a_unfolds = browser.find_element_by_xpath("//table[starts-with(@class,'VirusTable')]").find_element_by_tag_name("td").click()
unfolds = browser.find_element_by_xpath("//table[starts-with(@class,'VirusTable')]").find_elements_by_tag_name("tr")

for unfold in unfolds:
    try:
        a = unfold.find_element_by_tag_name("td")
        a.click()
    except:
        continue

browser.find_element_by_xpath("//table[starts-with(@class,'VirusTable')]").find_elements_by_tag_name("tr")
soup = BeautifulSoup(browser.page_source, 'html.parser')

time.sleep(4)
sqls = "INSERT OR REPLACE INTO virus ('datetime'"
sqle = ") VALUES ('" + now + "', "

city_sqls = "INSERT OR REPLACE INTO virus ('datetime'"
city_sqle = ") VALUES ('" + now + "', "
items = soup.find_all("tr")

conn = sqlite3.connect("virus.db")
cursor = conn.cursor()

for item in items:
    cityname = ""
    confirmed, recovered, death = 0, 0, 0,
    try:
        citylist = item.find_all("tr")
        for city in citylist:
            cityname = city.find_all("td")[0].text
            #print(cityname)
            if cityname in cityName.keys():
                confirmed = city.find_all("td")[1].text.strip()
                recovered = city.find_all("td")[2].text.strip()
                death = city.find_all("td")[3].text.strip()
                if recovered == "" or recovered == "-":
                    recovered = "0"
                if death == "" or death == "-":
                    death = "0"
                if confirmed == "" or confirmed == "-":
                    confirmed = "0"
                #cursor.execute("ALTER TABLE virus ADD " + cityName[cityname] + " CHAR(20);")
                print(cityname, cityName[cityname], confirmed, recovered, death)
                city_sqls += ", '" + cityName[cityname] + "'"
                city_sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "
    except:
        pass

for item in items:
    chname = ""
    confirmed, recovered, death = 0, 0, 0,
    try:
        chname = item.find_all("td")[0].text
    except:
        pass

    if (chname in placeName.keys()):
        confirmed = item.find_all("td")[1].text.strip()
        recovered = item.find_all("td")[2].text.strip()
        death = item.find_all("td")[3].text.strip()
        if recovered == "" or recovered == "-":
            recovered = "0"
        if death == "" or death == "-":
            death = "0"
        if confirmed == "" or confirmed == "-":
            confirmed = "0"
        print(chname, placeName[chname], confirmed, recovered, death)
        sqls += ", '" + placeName[chname].strip() + "'"
        sqle += "'" + confirmed + "-0-" + recovered + "-" + death + "', "

browser.close()

conn = sqlite3.connect("virus.db")
cursor = conn.cursor()

insert_record_sql = city_sqls + city_sqle[0: len(city_sqle) -2] + ")"
cursor.execute(insert_record_sql)

print("finished!")
