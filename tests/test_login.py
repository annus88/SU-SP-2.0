from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get(
    "http://127.0.0.1:5000/login"
)

driver.maximize_window()

driver.find_element(
    By.NAME,
    "email"
).send_keys("student@12")

driver.find_element(
    By.NAME,
    "password"
).send_keys("1234")

driver.find_element(
    By.TAG_NAME,
    "button"
).click()

time.sleep(3)

print(
    "Current Page:",
    driver.title
)

input("Press Enter to Close")

driver.quit()