# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 08:42:38 2024

@author: ppark
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pytz
import tkinter as tk
from tkinter import font as tkfont


# Run script at a specific time
kst = pytz.timezone('Asia/Seoul')
target_time = kst.localize(datetime(2024, 9, 20, 0, 0, 0))
#target_time = kst.localize(datetime(2024, 9, 19, 5, 22, 0)) # test timing
now = datetime.now(pytz.timezone('Asia/Seoul'))
time_to_wait = (target_time - now).total_seconds()

if time_to_wait > 0:
    time.sleep(time_to_wait)

print(f"Code is running at target time {target_time}  - KST.")

# Set up the WebDriver
driver = webdriver.Chrome()
driver.get("https://www.laneige.com/int/en/bespoke/reservation/reservation.html")
# for testing
#driver.get("<name of test file path>") # this was created by saving off a website's html

# Wait for the page to load#
#time.sleep(10)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.select-box .sel-label')))

# 1. Select the product "BESPOKE NEO Cushion 15g" <- not working
# try:
#     # Click the dropdown to open options
#     dropdown_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '.select-box .sel-label'))
#     )
#     driver.execute_script("arguments[0].click();", dropdown_button)

#     # Locate and click the desired option
#     option_to_select = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.XPATH, '//li[@data-value="0" and contains(text(), "BESPOKE NEO Cushion 15g (MATTE) - 45,000 KRW")]'))
#     )
#     driver.execute_script("arguments[0].click();", option_to_select)
    
#     # product_dropdown = driver.find_element(By.ID, "bespokeProductSelectbox")
#     # select_product = Select(product_dropdown)
#     # select_product.select_by_visible_text("BESPOKE NEO Cushion 15g (MATTE) - 45,000 KRW")
# except Exception as e:
#     print("Error selecting product:\n", e)

# 2. Select a valid date and time. (october)
dates = [20241026, 20241027, 20241029, 20241030]
times = [1100, 1140, 1220, 1400, 1440, 1520, 1600, 1700, 1740, 1820]
found = False

# 2a. Select a date (cycle through all possible dates)
for date_option in dates:
    print(date_option)
    date_select = driver.find_element(By.CSS_SELECTOR, f'input[type="radio"][value="{date_option}"]')
    driver.execute_script("arguments[0].click();", date_select) # click using JavaScript
    #date_select.click()
    
    if date_select.is_selected():
        # 2b. Select a time
        for time_option in times:
            print(time_option)
            time_select = driver.find_element(By.CSS_SELECTOR, f'input[type="radio"][value="{time_option}"]')
            driver.execute_script("arguments[0].click();", time_select) # click using JavaScript
            
            if time_select.is_selected(): #break loop if time is available
                found = True
                break
        
    if found: #break loop if a time AND date is available
        break

# 3. Fill in the "Name" fields
first_name_input = driver.find_element(By.ID, "userName_first")
first_name_input.send_keys("Brianna")

last_name_input = driver.find_element(By.ID, "userName_last")
last_name_input.send_keys("Huynh")

# 4. Fill in the "Email" field
email_input = driver.find_element(By.ID, "userEmail")
email_input.send_keys("paulrules66@yahoo.com.com")

# 5. Select the "I agree to all of them [Required]" checkbox
agree_checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox'][name='allagree']")  # Adjust the selector if needed
driver.execute_script("arguments[0].click();", agree_checkbox)

# 6. Select auth code button
email_auth_button = driver.find_element(By.ID, "form_verify")
email_auth_button.click()


# Submit the form (if there is a button to submit)
# submit_button = driver.find_element(By.ID, "submit_button_id")  # Adjust if needed
# submit_button.click()

# Wait for a few seconds to observe actions (optional)
#time.sleep(5)

# Close the browser
#driver.quit()
def create_message_window():
    root = tk.Tk()
    root.title("product Selection Reminder")
    custom_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
    message_label = tk.Label(root, text="SELECT A PRODUCT AND \nDOUBLE CHECK DATE/TIME", font = custom_font, padx=20, pady=20)
    message_label.pack()
    root.geometry("600x200")
    root.attributes('-topmost', 1)
    root.attributes('-topmost', 0)
    root.mainloop()

create_message_window()
