import platform

# TODO: upate this for macs
driver_mapping = {
    'Windows':'win32',
    'Linux':'linux64',
}

CHROME_DRIVER = '../res/chromedriver_' + driver_mapping[platform.system()] + '/chromedriver'


# Database Constants
FIREBASE_TOKEN_FILE = '../json/firebase.json'
FIREBASE_URL = 'https://library-room-auto-reserve.firebaseio.com'
FIREBASE_RESERVATIONS = 'reservations'
