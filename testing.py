from selenium import webdriver
from selenium.webdriver.common.by import By

# keep Chrome open after program finishes by configuring option and passing that as arg below
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.amazon.com/Book-Isaiah-Gods-Kingdom-Thematic-Theological-ebook/dp/B01M0M3KYF/?_encoding=UTF8&pd_rd_w=8IcUl&content-id=amzn1.sym.4ae371d4-7063-4b91-96b6-72c98af3e71b&pf_rd_p=4ae371d4-7063-4b91-96b6-72c98af3e71b&pf_rd_r=KH99EQN40TK2HNXM9JBJ&pd_rd_wg=feZiM&pd_rd_r=bd333d76-7253-43fb-8639-c16b7604691d&ref_=pd_hp_d_btf_BSDPUWYLOv1")

price = driver.find_element(by=By.ID, value='kindle-price').text

print(price)

# driver.close() - closes just one tab, quit closes the whole thing

# driver.quit()