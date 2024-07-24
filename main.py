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
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
actions = ActionChains(driver)

time.sleep(8)

start_time = time.time()
quittin_time = start_time + 60 * 1.1
lv = 0

# click big cookie, threaded
thread = threading.Thread(target=click_cookie)
thread.start()

while True:
    if lv == 10000:
        if time.time() > quittin_time:
            # driver.quit()
            break
        else:
            lv = 0

    # ------cookie-earning code------
    # click big cookie, unthreaded
    # big_cookie = driver.find_element(By.CSS_SELECTOR, value="#bigCookie")
    # big_cookie.click()

    # get current cookies - not doing anything with this variable currently
    cookie_count = driver.find_element(By.ID, "cookies").text.split("c")[0].replace(",", "")
    cookie_count = int(cookie_count)

    #------------------------------------------------------------------------------------------------------
    # click golden cookie
    try:
        golden_cookie = driver.find_element(By.CSS_SELECTOR, "#shimmers .shimmer")
        if golden_cookie:
            golden_cookie.click()
    except NoSuchElementException:
        pass

    #                               ------BUY THINGS------
    # ---------------------find upgrade with highest value and buy ----------------------------------------
    # im always getting stale ref errors when trying to click upgrades.
    try:
        upgrade = driver.find_element(By.CSS_SELECTOR, "#store #upgrades .enabled")
        upgrade.click()
    except NoSuchElementException or StaleElementReferenceException:
        pass

    # ---------------------find product with highest value and buy ----------------------------------------
    products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled .price")
    product_prices = [int(product.text.replace(",", "")) for product in products]
    if product_prices:
        max_value = max(product_prices)
        max_index = product_prices.index(max_value)
        grandparent_emendum = products[max_index].find_element(By.XPATH, "../..")
        grandparent_emendum.click()

    lv += 1
