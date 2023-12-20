from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.bikereg.com/events/")
driver.implicitly_wait(.5)

#fill out form
location = driver.find_element(by=By.ID, value="ctl00_ContentPlaceHolder1_cboRegion")
location.send_keys("NORTH CAROLINA")
search = driver.find_element(by=By.ID, value="ctl00_ContentPlaceHolder1_btnSearch")
search.click()



driver.implicitly_wait(10)