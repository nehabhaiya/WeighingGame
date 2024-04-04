from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def click_button(driver, button_text):
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{button_text}']")))
    button.click()

def fill_bowl(driver, bowl, bars):
    for i, bar in enumerate(bars):
        input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='{bowl}']//input[@class='goldInput'][{i+1}]")))
        input_field.clear()
        input_field.send_keys(str(bar))

def get_weighing_result(driver):
    return driver.find_element_by_id("weighResult").text

def get_alert_message(driver):
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        return alert.text
    except TimeoutException:
        return None

def perform_algorithm(driver):
    fake_bar = None
    weighing_count = 0
    weighing_list = []

    while not fake_bar:
        weighing_count += 1
        fill_bowl(driver, "leftBowl", [0, 1, 2])
        fill_bowl(driver, "rightBowl", [3, 4, 5])
        click_button(driver, "Weigh")
        weighing_list.append(get_weighing_result(driver))
        result = get_weighing_result(driver)
        if "left" in result:
            fake_bar = min(range(3), key=lambda x: x if x == 0 else -x)
        elif "right" in result:
            fake_bar = min(range(3), key=lambda x: x if x == 2 else -x)
        else:
            fake_bar = 2
        click_button(driver, "Reset")

    click_button(driver, str(fake_bar))
    alert_message = get_alert_message(driver)
    return fake_bar, alert_message, weighing_count, weighing_list

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Assuming you have Chrome WebDriver installed

# Open the website
driver.get("http://sdetchallenge.fetch.com/")

# Perform the algorithm
fake_bar, alert_message, weighing_count, weighing_list = perform_algorithm(driver)

# Output results
print(f"Found the fake gold bar is number {fake_bar}")
print(f"Alert Message: {alert_message}")
print(f"Number of Weighings: {weighing_count}")
print("List of Weighings:")
for i, result in enumerate(weighing_list, start=1):
    print(f"Weighing {i}: {result}")

# Close the browser
driver.quit()
