import platform
import os

def get_from_cache(variable, callback, *args):
    if variable not in os.environ:
        os.environ['variable'] = callback(args)
    return os.environ[variable]


# TODO: upate this for macs
driver_mapping = {
    'Windows':'win32',
    'Linux':'linux64',
}

CHROME_DRIVER = './res/chromedriver_' + driver_mapping[platform.system()] + '/chromedriver'
