import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from database_access import add_reservation
from constants import CHROME_DRIVER
import re
from pprint import pprint

# General Constants


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
    book_rooms()


def book_rooms():
    # Setup selenium
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=options)
    browser.get(CATALOG_URL)

    # Extract time slots into a matrix
    matrix = get_slots_matrix(browser)
    pprint (matrix)

    # Compute optimal range of slots
    optimal = get_optimal_range(matrix)

    # Start booking
    select_slots(browser, optimal)

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
                title = slot.get_attribute("title")
                room = title[:4]
                date = re.search(r'[^,]+,[^,]+$', title).group()
                starttime = re.findall(r'\d:\d[^\s,]+', title)[0]
                endtime = re.findall(r'\d:\d[^\s,]+', title)[1]
                open_slots.append((index, room, date, starttime, endtime))
        matrix.append(open_slots)
    return matrix


# Get optimal time range for room reservation
#Pick rooms based on the following criteria:
#1. Reserve the same room as the last reservation in the database, if possible
#2. Reserve the room with the most consecutive open slots, otherwise
def get_optimal_range(matrix):
    optimal = []
    num_picked = 0

    #STUB CODE
    #picks the first 4 open spots in the first open room
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            cell = matrix[i][j] #uses row 1 bc row 0 is empty
            optimal.append( (i, *cell) ) #optimal -> (row, index, room, date, starttime, endtime)
            num_picked+=1
            if num_picked == 4:
                return optimal


    return None


# Select and submit slots on browser
def select_slots(browser, optimal):
    table = browser.find_element_by_id(TIME_TABLE_ID)
    rows = table.find_elements_by_xpath(".//tbody/*")

    for i in range(len(rows)):

        select = list(filter(lambda x: x[0] == i, optimal))
        good_clicks=0
        if len(select) != 0:
            row = rows[i]
            slots = row.find_elements_by_xpath(".//td/*")
            for j in select:
                index = j[1]
                room = j[2]
                date = j[3]
                starttime = j[4]
                endtime = j[5]

                slots[index].click()
                good_clicks += 1
                print(room, date, starttime, endtime, USERNAME)
                add_reservation(room, date, starttime, endtime, USERNAME)
                time.sleep(1)
                if good_clicks == 4:
                    break


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
