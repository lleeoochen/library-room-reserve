import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# General Constants
CHROME_DRIVER = './res/chromedriver'
CATALOG_URL = 'http://libcal.library.ucsb.edu/booking/groupstudy'
STUDY_ROOM_NAME = 'it really do be like that sometimes'
USERNAME = os.environ['UMAIL_USERNAME']
PASSWORD = os.environ['UMAIL_PASSWORD']

# HTML Page Constants
TIME_TABLE_ID = 's-lc-rm-scrolltb'
ROOM_TABLE_ID = 's-lc-rm-tg-rnames'
ROOM_LABEL_CLASS = 's-lc-rm-rntd'
CONTINUE_BUTTON_ID = 'rm_tc_cont'
SUBMIT_BUTTON_ID = 's-lc-rm-sub'
USERNAME_FIELD_ID = 'username'
PASSWORD_FIELD_ID = 'password'
ROOMNAME_FIELD_ID = 'nick'


# Main Scraper Program
def main():
    # Setup selenium
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=options)
    browser.get(CATALOG_URL)

    # Extract time slots into a matrix
    matrix = get_slots_matrix(browser)
    print (matrix)

    # Compute optimal range of slots
    slots_range = get_optimal_range(matrix)

    # Start booking
    select_slots(browser, matrix)

    # Authenticate
    authenticate(browser, USERNAME, PASSWORD)

    # Finalize booking
    time.sleep(3)
    finalize_booking(browser)

    # Exit browser
    time.sleep(5)
    browser.quit()


# Get a 2D matrix of available time slots 
def get_slots_matrix(browser):
    table = browser.find_element_by_id(TIME_TABLE_ID)
    rows = table.find_elements_by_xpath(".//tbody/*")
    matrix = []
    for row in rows:
        open_slots = []
        slots = row.find_elements_by_xpath(".//td/*")
        for index, slot in enumerate(slots):
            if slot.tag_name == 'a':
                open_slots.append(index)
        matrix.append(open_slots)
    return matrix


# Get optimal time range for room reservation
def get_optimal_range(matrix):
    return None


# Select and submit slots on browser
def select_slots(browser, matrix):
    table = browser.find_element_by_id(TIME_TABLE_ID)
    rows = table.find_elements_by_xpath(".//tbody/*")
    for i in range(len(rows)):
        row = rows[i]
        slots = row.find_elements_by_xpath(".//td/*")
        for j in matrix[i]:
            try: slots[j].click()
            except: pass

    time.sleep(1)
    continue_button = browser.find_element_by_id(CONTINUE_BUTTON_ID)
    continue_button.click()

    time.sleep(1)
    submit_button = browser.find_element_by_id(SUBMIT_BUTTON_ID)
    submit_button.click()


# UCSB authentication
def authenticate(browser, username, password):
    time.sleep(1)
    username_field = browser.find_element_by_id(USERNAME_FIELD_ID)
    username_field.send_keys(username)
    
    time.sleep(1)
    password_field = browser.find_element_by_id(PASSWORD_FIELD_ID)
    password_field.send_keys(password)

    time.sleep(1)
    submit_button = browser.find_element_by_name('submit')
    submit_button.click()


# UCSB finalize booking
def finalize_booking(browser):
    time.sleep(1)
    roomname_field = browser.find_element_by_id(ROOMNAME_FIELD_ID)
    roomname_field.send_keys(STUDY_ROOM_NAME)

    time.sleep(1)
    submit_button = browser.find_element_by_name('Submit')
    submit_button.click()


# Entry point for main
if __name__ == '__main__':
    main()
