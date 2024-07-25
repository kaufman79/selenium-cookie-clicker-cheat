from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import threading
import csv
import os


# Notes:
""" 
- Cookie clicker saves your save in a cookies file. Selenium can handle this with the line `chrome_options.add_argument("user-data-dir=fresh_start")`
which saves those files in a folder in the project dir. Before first run, youll want to set start
delay to a high value so you can go in, select your language and change some necessary settings.
- in settings, you must change screen reader mode to on for the upgrades (not buildings) to work. 
You should also change Short Numbers to off, in case you ever get into the millions, which would break
certain lines.
"""

# variables that effect performance, to write into csv
MINUTES_RUN = 5
LOOPS_PER_CYCLE = 400
DELAY_PER_CYCLE = 7

file_exists = os.path.isfile("results.csv")


def append_csv():
    with open("results.csv", mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "minutes_run",
            "loops/cycle",
            "delay/cycle",
            "final_cookies/second"
            ])

        if not file_exists:
            writer.writeheader()

        data = [{
            "minutes_run": MINUTES_RUN,
            "loops/cycle": LOOPS_PER_CYCLE,
            "delay/cycle": DELAY_PER_CYCLE,
            "final_cookies/second": cookies_per_second
        }]

        for row in data:
            writer.writerow(row)


def reset():
    """
     goes to options to wipe save, then saves game, exits options
    """
    driver.find_element(By.CSS_SELECTOR, value="#prefsButton").click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, value=".warning").click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, value='#promptOption0').click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, value='#promptOption0').click()
    time.sleep(0.5)
    # save:
    driver.find_element(By.XPATH, '//*[@id="menu"]/div[3]/div/div[3]/a').click()
    driver.find_element(By.CSS_SELECTOR, value="#prefsButton").click()


class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        big_cookie = driver.find_element(By.CSS_SELECTOR, value="#bigCookie")
        while not self._stop_event.is_set():
            big_cookie.click()
        print("Thread is stopping")

    def stop(self):
        self._stop_event.set()


# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
# load cookies, ie save file
chrome_options.add_argument("user-data-dir=fresh_start")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
actions = ActionChains(driver)

start_delay = 10
time.sleep(start_delay)

start_time = time.time()
quittin_time = start_time + 60 * MINUTES_RUN
loop_nr = 0
cycle = 1

thread = StoppableThread()
thread.start()

print("cycle: ", cycle)

while True:
    if time.time() > quittin_time:
        thread.stop()
        cookies_per_second = driver.find_element(By.CSS_SELECTOR, "#cookiesPerSecond").text
        cookies_per_second = cookies_per_second.split(" ")[2]
        print("cookies ", cookies_per_second)
        reset()
        append_csv()
        # driver.quit()
        break

    if loop_nr == LOOPS_PER_CYCLE:
        cycle += 1
        print("cycle: ", cycle)
        loop_nr = 0
        time.sleep(DELAY_PER_CYCLE)

    # ------cookie-earning code------

    # -------get current cookies - not doing anything with this variable currently
    # cookie_count = driver.find_element(By.ID, "cookies").text.split("c")[0].replace(",", "")
    # cookie_count = int(cookie_count)

    # ------------------------------------------------------------------------------------------------------
    # click golden cookie
    # try:
    #     golden_cookie = driver.find_element(By.CSS_SELECTOR, "#shimmers .shimmer")
    #     if golden_cookie:
    #         golden_cookie.click()
    # except NoSuchElementException:
    #     pass

    #                               ------BUY THINGS------
    # ---------------------buy upgrades, start with priciest ---------------------------
    try:
        upgrades = driver.find_elements(By.CSS_SELECTOR, "#store #upgrades .enabled")
        for i in range(len(upgrades) - 1, -1, -1):
            upgrades[i].click()
    except (NoSuchElementException, StaleElementReferenceException):
        pass

    # ---------------------find product with highest value and buy ----------------------------------------
    products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled .price")
    product_prices = [int(product.text.replace(",", "")) for product in products]
    if product_prices:
        max_value = max(product_prices)
        max_index = product_prices.index(max_value)
        grandparent_to_buy = products[max_index].find_element(By.XPATH, "../..")
        grandparent_to_buy.click()

    # loop count
    loop_nr += 1
