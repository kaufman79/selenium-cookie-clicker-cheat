from selenium import webdriver
from selenium.webdriver.common.by import By

# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://en.wikipedia.org/wiki/Main_Page")

# for CSS selector, put a period before CSS stuff, a # before id
num_articles = driver.find_element(By.CSS_SELECTOR,
                                   "#mp-welcomecount #articlecount a")

print(num_articles.text)

driver.quit()
