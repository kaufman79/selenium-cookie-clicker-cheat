from selenium import webdriver
from selenium.webdriver.common.by import By

# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://python.org")

search_bar = driver.find_element(by=By.NAME, value='q')

# print(search_bar.tag_name)
print(search_bar.get_attribute("placeholder"))  # returns 'search'

# documentation_link = driver.find_element(By.CSS_SELECTOR,
#                                          value=".documentation-widget a")
# print(documentation_link.text)

# finding by XPath
pep_index = driver.find_element(By.XPATH, '//*[@id="container"]/li[3]/ul/li[7]/a')
print(pep_index.text)


# driver.close() - closes just one tab, quit closes the whole thing

driver.quit()