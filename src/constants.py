import platform



def get_driver():
    if "Microsoft" in platform.version():
        return 'win32/chromedriver.exe' #a thing you have to do for WSL

    # TODO: upate this for macs
    driver_mapping = {
        'Windows':'win32/chromedriver.exe',
        'Linux':'linux64/chromedriver',
    }
    return driver_mapping[platform.system()]

CHROME_DRIVER = 'res/chromedriver_' + get_driver()


#Email Constants
EMAIL_ACCESS_TOKEN = 'json/token.json'
EMAIL_CREDENTIALS = 'json/credentials.json'


# Database Constants
FIREBASE_TOKEN_FILE = 'json/firebase.json'
FIREBASE_URL = 'https://library-room-auto-reserve.firebaseio.com'
FIREBASE_RESERVATIONS = 'reservations'
