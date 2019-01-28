import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from . import  database_access as db
from .constants import CHROME_DRIVER
import re
from pprint import pprint
from datetime import datetime
from datetime import timedelta

# General Constants


CATALOG_URL = 'http://libcal.library.ucsb.edu/booking/groupstudy'
# CATALOG_URL = 'https://libcal.library.ucsb.edu/booking/24hour'
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
MONTH_PICKER_CLASS = 'ui-datepicker-month'
DATE_PICKER_CLASS = 'ui-datepicker-calendar'

# Main Scraper Program
def main():

    num_picked = book_rooms()
    return num_picked

# TODO: plz modify this so that it books the rooms for the given date
# date is a datetime object
def book_rooms():

    # Setup selenium
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=options)

    count=0
    date = get_resevation_date_for(USERNAME)
    print (date)
    while date < datetime.today() + timedelta(days=14):

        browser.get(CATALOG_URL)

        time.sleep(5)

        optimal = None
        while optimal == None:

            # Select date
            sucessful = select_date(browser, date)
            if not sucessful:
                browser.quit()
                return count

            # Extract time slots into a matrix
            matrix = get_slots_matrix(browser)

            # Compute optimal range of slots
            optimal = get_optimal_range(matrix)

            # Increment to next day if current date has no optimal spot
            if optimal == None:
                date += timedelta(days=1)


        pprint(optimal)
        # Start booking
        select_slots(browser, optimal)

        # Authenticate
        if count == 0:
            authenticate(browser, USERNAME, PASSWORD)

        # Finalize booking
        time.sleep(1)
        finalize_booking(browser)

        # Exit browser
        time.sleep(3)
        date = get_resevation_date_for(USERNAME)
        count+=1
        print("Next date: " + str(date))
        print("Max date: " + str(date < datetime.today() + timedelta(days=14)))
    browser.quit()
    return count

# Select date on website
def select_date(browser, date):
    try:
        browser.find_element_by_xpath("//select[@class='" + MONTH_PICKER_CLASS + "']/option[@value='" + str(date.month - 1) + "']").click()
        browser.find_element_by_xpath("//table[@class='" + DATE_PICKER_CLASS + "']//*[text()[contains(.,'" + str(date.day) + "')]]").click()
        time.sleep(2)
        return True
    except Exception as e:
        return False


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
                starttime = re.findall(r'\d+:\d[^\s,]+', title)[0]
                endtime = re.findall(r'\d+:\d[^\s,]+', title)[1]
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

    reservations = db.get_all_reservations()
    for r in reservations:
        r['date'] = datetime.strptime(r['date'], " %B %d, %Y")
        # r['starttime'] = datetime.strptime(r['date'], " %B %d, %Y")
        # r['endtime'] = datetime.strptime(r['date'], " %B %d, %Y")


    pick_room = check_old_room(matrix, reservations)
    print (pick_room)
    if pick_room == -1:
        pick_room = find_most_consecutive_slots(matrix)

    #i know this code is really shitty and doesnt always work like i want it to, but im lazy and its good enough
    for j in range(len(matrix[pick_room])):
        cell = matrix[pick_room][j] #uses row 1 bc row 0 is empty
        optimal.append( (pick_room, *cell) ) #optimal -> (row, index, room, date, starttime, endtime)
        num_picked+=1
        if num_picked == 4:
            return optimal



    return None

def check_old_room(matrix, reservations):
    most_recent = max(reservations, key=lambda x: x['date'])

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            cell = matrix[i][j]
            if cell[1] == most_recent['room']: # and cell[3] == most_recent['endtime']:#picking up after the last reservation
                return i
    return -1

#I also know this function does not work as intended but its good enough
def find_most_consecutive_slots(matrix):
    most = 0
    for i in range(len(matrix)):
        length = len(matrix[i])
        if length > len(matrix[most]):
            most = i
    return most

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
                db.add_reservation(room, date, starttime, endtime, USERNAME)
                # time.sleep(1)
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

#Finds the date that the given user should be reserving
#returns a datetime object
def get_resevation_date_for(user):
    reservations = db.get_reservations_for(user)
    dates = [datetime.strptime(r['date'], " %B %d, %Y") for r in reservations]

    if len(dates) > 0 and max(dates) >= datetime.today():
        most_recent = max(dates)
        return most_recent + timedelta(days=1)
    else:
        return datetime.today()


# Entry point for main
if __name__ == '__main__':
    main()
