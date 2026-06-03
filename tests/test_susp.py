from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()

driver.maximize_window()

BASE_URL = "http://127.0.0.1:5000"

# ==========================================
# AUTHENTICATION TESTING
# ==========================================

driver.get(BASE_URL + "/register")

time.sleep(2)

driver.find_element(
    By.NAME,
    "username"
).send_keys("selenium_student")

driver.find_element(
    By.NAME,
    "email"
).send_keys("selenium@student.com")

driver.find_element(
    By.NAME,
    "password"
).send_keys("12345678")

Select(
    driver.find_element(
        By.NAME,
        "role"
    )
).select_by_visible_text("Student")

driver.save_screenshot(
    "01_registration_page.png"
)

driver.find_element(
    By.TAG_NAME,
    "form"
).submit()

time.sleep(2)

driver.save_screenshot(
    "02_registration_success.png"
)

# ==========================================
# LOGIN TEST
# ==========================================

driver.get(BASE_URL + "/login")

driver.find_element(
    By.NAME,
    "email"
).send_keys("selenium@student.com")

driver.find_element(
    By.NAME,
    "password"
).send_keys("12345678")

driver.find_element(
    By.TAG_NAME,
    "form"
).submit()

time.sleep(3)

driver.save_screenshot(
    "03_login_success.png"
)

# ==========================================
# STUDENT MODULE
# ==========================================

driver.get(BASE_URL + "/courses")

time.sleep(2)

driver.save_screenshot(
    "04_course_enrollment.png"
)

driver.get(BASE_URL + "/assignment")

time.sleep(2)

driver.save_screenshot(
    "05_assignment_page.png"
)

driver.get(BASE_URL + "/status")

time.sleep(2)

driver.save_screenshot(
    "06_assignment_status.png"
)

driver.get(BASE_URL + "/grades")

time.sleep(2)

driver.save_screenshot(
    "07_view_grades.png"
)

# ==========================================
# LOGOUT
# ==========================================

driver.get(BASE_URL + "/logout")

time.sleep(2)

driver.save_screenshot(
    "08_logout_success.png"
)

# ==========================================
# TEACHER LOGIN
# ==========================================

driver.get(BASE_URL + "/login")

driver.find_element(
    By.NAME,
    "email"
).send_keys("usman@12")

driver.find_element(
    By.NAME,
    "password"
).send_keys("1234")

driver.find_element(
    By.TAG_NAME,
    "form"
).submit()

time.sleep(3)

driver.save_screenshot(
    "09_teacher_dashboard.png"
)

# ==========================================
# CREATE ASSIGNMENT
# ==========================================

driver.get(
    BASE_URL +
    "/teacher/create_assignment"
)

time.sleep(2)

driver.save_screenshot(
    "10_create_assignment.png"
)

# ==========================================
# REVIEW SUBMISSION
# ==========================================

driver.get(
    BASE_URL +
    "/teacher/review"
)

time.sleep(2)

driver.save_screenshot(
    "11_review_submission.png"
)

# ==========================================
# MANAGE COURSES
# ==========================================

driver.get(
    BASE_URL +
    "/teacher/courses"
)

time.sleep(2)

driver.save_screenshot(
    "12_manage_courses.png"
)

# ==========================================
# ADMIN LOGIN
# ==========================================

driver.get(BASE_URL + "/logout")

driver.get(BASE_URL + "/login")

driver.find_element(
    By.NAME,
    "email"
).send_keys("admin@12")

driver.find_element(
    By.NAME,
    "password"
).send_keys("1234")

driver.find_element(
    By.TAG_NAME,
    "form"
).submit()

time.sleep(3)

driver.save_screenshot(
    "13_admin_dashboard.png"
)

# ==========================================
# MANAGE USERS
# ==========================================

driver.get(
    BASE_URL +
    "/admin/users"
)

time.sleep(2)

driver.save_screenshot(
    "14_manage_users.png"
)

# ==========================================
# ASSIGN ROLES
# ==========================================

driver.get(
    BASE_URL +
    "/admin/roles"
)

time.sleep(2)

driver.save_screenshot(
    "15_assign_roles.png"
)

# ==========================================
# MONITORING
# ==========================================

driver.get(
    BASE_URL +
    "/admin/monitor"
)

time.sleep(2)

driver.save_screenshot(
    "16_system_monitoring.png"
)

# ==========================================
# REPORTS
# ==========================================

driver.get(
    BASE_URL +
    "/admin/reports"
)

time.sleep(2)

driver.save_screenshot(
    "17_reports.png"
)

# ==========================================
# FINAL RESULT
# ==========================================

driver.save_screenshot(
    "18_test_execution_result.png"
)

print(
    "ALL TEST CASES EXECUTED SUCCESSFULLY"
)

time.sleep(2)

driver.quit()