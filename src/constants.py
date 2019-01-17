import platform

# TODO: upate this for macs
driver_mapping = {
    'Windows':'win32',
    # 'Linux':'linux64',
    'Linux':'win32', #some weird hacky shit you have to do for WSL. will figure it out eventually
}

CHROME_DRIVER = 'res/chromedriver_' + driver_mapping[platform.system()] + '/chromedriver.exe'


#Email Constants
EMAIL_ACCESS_TOKEN = 'json/token.json'
EMAIL_CREDENTIALS = 'json/credentials.json'


# Database Constants
FIREBASE_TOKEN_FILE = 'json/firebase.json'
FIREBASE_URL = 'https://library-room-auto-reserve.firebaseio.com'
FIREBASE_RESERVATIONS = 'reservations'
