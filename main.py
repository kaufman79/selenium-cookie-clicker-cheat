from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import threading


# variables that effect performance, to write into csv
MINUTES_RUN = 1
LOOPS_PER_CYCLE = 300
DELAY_PER_CYCLE = 10

# ---

def write_CSV():
    pass

def reset():
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

start_delay = 35
time.sleep(start_delay)

start_time = time.time()
quittin_time = start_time + 60 * MINUTES_RUN
loop_nr = 0
cycle = 1

thread = StoppableThread()
thread.start()

print("cycle: ", cycle)

while True:
    if loop_nr == LOOPS_PER_CYCLE:
        cycle += 1
        print("cycle: ", cycle)
        if time.time() > quittin_time:
            thread.stop()
            cookies_per_second = driver.find_element(By.CSS_SELECTOR, "#cookiesPerSecond").text
            print("cookies ", cookies_per_second)

            # ----------the following code will wipe the save to start fresh next time--------------
            reset()

            time.sleep(0.5)
            # driver.quit()
            break
        else:
            loop_nr = 0
            time.sleep(DELAY_PER_CYCLE)

    # ------cookie-earning code------
    # click big cookie, unthreaded
    # big_cookie = driver.find_element(By.CSS_SELECTOR, value="#bigCookie")
    # big_cookie.click()

    # get current cookies - not doing anything with this variable currently
    # cookie_count = driver.find_element(By.ID, "cookies").text.split("c")[0].replace(",", "")
    # cookie_count = int(cookie_count)

    #------------------------------------------------------------------------------------------------------
    # click golden cookie
    # try:
    #     golden_cookie = driver.find_element(By.CSS_SELECTOR, "#shimmers .shimmer")
    #     if golden_cookie:
    #         golden_cookie.click()
    # except NoSuchElementException:
    #     pass

    #                               ------BUY THINGS------
    # ---------------------buy upgrades, start with cheapest ---------------------------
    try:
        upgrades = driver.find_elements(By.CSS_SELECTOR, "#store #upgrades .enabled")
        for upgrade in upgrades:
            upgrade.click()
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
