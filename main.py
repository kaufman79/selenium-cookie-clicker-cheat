from selenium import webdriver
from selenium.webdriver.common.by import By
import time



# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://orteil.dashnet.org/cookieclicker/")
time.sleep(12)

five_minutes_hence = time.time() + 60*5
lv = 0
while True:
    if lv == 1000:
        if time.time() > five_minutes_hence:
            break
        else:
            lv = 0

    print(lv)

    lv += 1
