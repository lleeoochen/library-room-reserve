import pip

packages = {
    'selenium': 0,
    'firebase_admin': 0,
    'requests': 0,
    'python-firebase': 0,
    'google-api-python-client': 0,
    'oauth2client': 0
}

for package in packages:
    packages[package] = pip.main(['install', package])

print ('\n----- Download Summary -----\n')
for package, status in packages.items():
    print (package.upper() + ' \tDownloaded: ' + str(status == 1))
