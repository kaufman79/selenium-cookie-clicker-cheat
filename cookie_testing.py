from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import threading
import csv
import os
import math


"""
Note to user: 
- Cookie clicker saves your save in a cookies file. Selenium can handle this with 
the line `chrome_options.add_argument("user-data-dir=fresh_start")`
which saves those files in a folder in the project dir. Before first run, you'll want to set start
delay to a high value so you can go in, select your language and change some necessary settings.
- in settings, you may have to change screen reader mode to on for the upgrades (not buildings) to work. 
You should also change Short Numbers to off, in case you ever get into the millions, which would break
certain lines of code.
- clicking a golden cookie, should it come up, is possible, but that code is currently commented
out, since the point of this code is to test the algorithm and compare results, which RNG would skew.
- some ideas to implement: 
    - place the building buying outside of the main loop, and just buy buildings every so often. Though
    the same effect can sorta be achieved with lowering loops per cycle and adding delay.
    - buy most advanced (lowest in list) building option, or prioritize grandmas maybe. not cursors after x number.
"""

# ---------------variables that affect algorithm performance---------------
MINUTES_RUN = 5
DELAY_PER_LOOP = 0
LOOPS_PER_CYCLE = 1000
DELAY_PER_CYCLE = 4
D_INC_RATE = 1.3  # delay increase rate
D_INC_TYPE = 1  # 0 for linear, 1 for quadratic, 2 for logarithmic
TARGET_CURSORS = 10
CALC_BUY_PERCENT = 0.80  # see calculated_buy function; buys buildings only if theyre x% cheaper than the next
# -------------------------------------------------------------------------
start_delay = 33


def calculated_buy():
    """
    check the prices of buildings; if current building costs < x% of the next building,
    buy current building.
    """
    price_elements = driver.find_elements(By.CSS_SELECTOR, "#products .unlocked .price")
    product_prices = [int(product.text.replace(",", "")) for product in price_elements]
    if len(product_prices) > 2:
        for i in range(0, len(product_prices) - 1):
            price_current = product_prices[i]
            price_next = product_prices[i + 1]
            if price_current < CALC_BUY_PERCENT * price_next and can_afford(price_current):
                # clicks on the grandparent element, i.e. the clickable element
                price_elements[i].find_element(By.XPATH, "../..").click()
                break
    else:  # buy anything possible
        products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled")
        if products:
            products[0].click()


def can_afford(item_int):
    cookies_current = get_total_cookies()
    if cookies_current >= item_int:
        return True
    else:
        return False


def get_total_cookies():
    while True:
        try:
            cookie_count = driver.find_element(By.ID, "cookies").text.split("c")[0].replace(",", "")
            return int(cookie_count)
        except StaleElementReferenceException:
            time.sleep(0.1)


def get_cps(driver_instance):
    while True:
        try:
            cps_element = driver_instance.find_element(By.CSS_SELECTOR, "#cookiesPerSecond")
            cps = cps_element.text
            cps = cps.split(" ")[2]
            return cps
        except StaleElementReferenceException:
            time.sleep(0.1)


def append_csv():
    file_exists = os.path.isfile("results.csv")
    with open("results.csv", mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "minutes_run",
            "delay/loop",
            "loops/cycle",
            "base_delay/cycle",
            "delay_increase_rate",
            "delay_increase_type",
            "target_cursors",
            "final_cookies/second",
            "notes"
            ])

        if not file_exists:
            writer.writeheader()

        data = [{
            "minutes_run": MINUTES_RUN,
            "loops/cycle": LOOPS_PER_CYCLE,
            "delay/loop": DELAY_PER_LOOP,
            "base_delay/cycle": DELAY_PER_CYCLE,
            "delay_increase_rate": D_INC_RATE,
            "delay_increase_type": D_INC_TYPE,
            "target_cursors": TARGET_CURSORS,
            "final_cookies/second": cookies_per_second,
            "notes": ""
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


chrome_options = webdriver.ChromeOptions()
# load cookies, ie save file
chrome_options.add_argument("user-data-dir=fresh_start")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(start_delay)

start_time = time.time()
quittin_time = start_time + 60 * MINUTES_RUN
loop_nr = 0
cycle = 1

hit_target_cursors = False

thread = StoppableThread()
thread.start()

print("cycle: ", cycle)

while True:
    if time.time() > quittin_time:
        thread.stop()
        cookies_per_second = get_cps(driver)
        print("cookies per second: ", cookies_per_second)
        reset()
        append_csv()
        # driver.quit()
        break

    if loop_nr == LOOPS_PER_CYCLE:
        cycle += 1
        print("cycle: ", cycle)
        loop_nr = 0
        # ---------------cycle delay---------------
        match D_INC_TYPE:
            case 0:  # linear
                cycle_delay = DELAY_PER_CYCLE + (cycle - 1) * D_INC_RATE
            case 1:  # quadratic
                cycle_delay = DELAY_PER_CYCLE + D_INC_RATE * (cycle - 1)**2
            case 2:  # logarithmic
                cycle_delay = DELAY_PER_CYCLE + D_INC_RATE * math.log(cycle + 1)

        if cycle_delay > quittin_time - time.time():
            cycle_delay = quittin_time - time.time() - 1
            print("shortening delay")
        time.sleep(cycle_delay)
        print("cycle delay was", cycle_delay)

    # ------cookie-earning code------

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
        for i in range(0, len(upgrades), 1):
            upgrades[i].click()
    except (NoSuchElementException, StaleElementReferenceException):
        pass

    # -----------------find products and buy, starting with most advanced --------------------
    # if not hit_target_cursors:  # buy any, including cursors
    #     products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled")
    #     if products:
    #         for i in range(min(2, len(products) - 1), -1, -1):
    #             products[i].click()
    #
    #     # get cursors owned number
    #     cursor_text = driver.find_element(By.CSS_SELECTOR, "#store #products #productOwned0").text
    #     if cursor_text == "":
    #         nr_cursors = 0
    #     else:
    #         nr_cursors = int(cursor_text)
    #
    #     if nr_cursors == TARGET_CURSORS:
    #         hit_target_cursors = True

    # else:  # dont buy cursors
        # products = driver.find_elements(By.CSS_SELECTOR, "#products .enabled")
        # if products:
        #     for i in range(min(2, len(products) - 1), 0, -1):
        #         products[i].click()
    calculated_buy()

    time.sleep(DELAY_PER_LOOP)
    # loop count
    loop_nr += 1
