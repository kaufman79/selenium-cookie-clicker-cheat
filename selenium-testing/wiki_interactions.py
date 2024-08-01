from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://en.wikipedia.org/wiki/Main_Page")

# find element by link text
# all_portals = driver.find_element(By.LINK_TEXT, "Content portals")
#
# all_portals.click()

# if link were to open in new tab, switch to that tab with the following:
# driver.switch_to.window(driver.window_handles[1])

searchbar = driver.find_element(By.NAME, "search")
searchbar.send_keys("Python", Keys.ENTER)


driver.find_element(By.LINK_TEXT, "Python (programming language)").click()


# driver.quit()
