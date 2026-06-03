from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get(
    "http://127.0.0.1:5000/login"
)

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

time.sleep(2)

driver.get(
    "http://127.0.0.1:5000/courses"
)

time.sleep(2)

driver.save_screenshot(
    "course_enrollment.png"
)

input("Press Enter")

driver.quit()