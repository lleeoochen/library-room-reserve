import platform

# TODO: upate this for macs
driver_mapping = {
    'Windows':'win32',
    'Linux':'linux64',
}

CHROME_DRIVER = './res/chromedriver_' + driver_mapping[platform.system()] + '/chromedriver'
