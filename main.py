from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import threading


def click_cookie():
    big_cookie = driver.find_element(By.CSS_SELECTOR, value="#bigCookie")
    while True:
        big_cookie.click()


# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
# load cookies, ie save file
chrome_options.add_argument("user-data-dir=fresh_start")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
actions = ActionChains(driver)

time.sleep(10)


start_time = time.time()
quittin_time = start_time + 60 * 0.3
lv = 0
cycle = 1

# --------------------click big cookie, threaded--------------------
big_cookie = driver.find_element(By.CSS_SELECTOR, value="#bigCookie")


class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            big_cookie.click()
        print("Thread is stopping")

    def stop(self):
        self._stop_event.set()


thread = StoppableThread()
thread.start()
# --------------------end of click big cookie, threaded--------------------


print("cycle: ", cycle)

while True:
    if lv == 1000:
        cycle += 1
        print("cycle: ", cycle)
        if time.time() > quittin_time:
            thread.stop()
            print("cookies ", driver.find_element(By.CSS_SELECTOR, "#cookiesPerSecond").text)
            # ----------the following code will wipe the save to start fresh next time--------------
            driver.find_element(By.CSS_SELECTOR, value="#prefsButton").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, value=".warning").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, value='#promptOption0').click()
            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, value='#promptOption0').click()
            driver.find_element(By.CSS_SELECTOR, value="#prefsButton").click()
            # driver.quit()
            break
        else:
            lv = 0
            time.sleep(30)

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
    # ---------------------find upgrade with highest value and buy ----------------------------------------
    #
    try:
        upgrade = driver.find_element(By.CSS_SELECTOR, "#store #upgrades .enabled")
        upgrade.click()
    except (NoSuchElementException, StaleElementReferenceException):
        pass

    # ---------------------find product with highest value and buy ----------------------------------------
    products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled .price")
    product_prices = [int(product.text.replace(",", "")) for product in products]
    if product_prices:
        max_value = max(product_prices)
        max_index = product_prices.index(max_value)
        grandparent_emendum = products[max_index].find_element(By.XPATH, "../..")
        grandparent_emendum.click()

    # loop count
    lv += 1
