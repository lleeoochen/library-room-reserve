from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from constants import CHROME_DRIVER


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    confirm_from_email()




def confirm_from_email():
    service = authorize()
    url = get_confirmation_url(service)
    click_confirmation(url)


def click_confirmation(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=options)
    browser.get(url)


    confirm_button = browser.find_element_by_id("rm_confirm_link")
    confirm_button.click()


def get_confirmation_url(service):

    counter =0

    done = False
    while not done:
        if counter > 3: #try 3 times before giving up
            return None

        # results = service.users().messages().list(userId='me', q="from:alerts@mail.libcal.com newer_than:1d subject:Please confirm your booking!").execute()
        results = service.users().messages().list(userId='me', q="from:alerts@mail.libcal.com subject:Please confirm your booking!").execute()
        if results['resultSizeEstimate'] > 0:
            done = True
        else:
            print("Confirmation Email Not Found...")
            # sleep(5 * 60) #sleep for 5 minutes before trying again
            sleep(5)
            counter+=1



    confirmation_id = results['messages'][0]['id']
    confirmation =service.users().messages().get(userId='me', id=confirmation_id).execute()
    url = re.search("http[^\s]+", confirmation['snippet']).group(0)
    url = re.sub("&amp;", "&", url)

    return url


def authorize():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('json/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('json/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

if __name__ == '__main__':
    main()
