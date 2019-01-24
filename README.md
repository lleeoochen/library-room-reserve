TODO:
* fix time regex
* change reservation code to work with arbitrary dates
* test chrome drivers for MacOS
* figure out how to schedule code to run every 24 hours
* streamline setup process


## Setup
  1. Install Python Selenium package: 
```
  sudo pip install selenium
```
  2. Install Python Firebase packages:
```
  sudo pip install firebase_admin
  sudo pip install requests
  sudo pip install python-firebase
```
  3. Add UCSB username and password to env variables (in ~/.bashrc or ~/.bash_profile)
```
  export UMAIL_USERNAME=[Your UCSB Username]
  export UMAIL_PASSWORD=[Your UCSB Password]
```
  4. Run `source ~/.bashrc` or `source ~/.bash_profile` to take changes into effect.

  5. Install Gmail packages
```
  sudo pip install oauth2client
  sudo pip install google-api-python-client
  sudo pip install httplib2
```
  6. Complete Gmail Authentication flow
```
  python do_auth.py --noauth_local_webserver
```

  7. Use chron to schedule task
  run `chrontab -e`
  type `5 0 * * *  /usr/bin/python /path/to/main.py`


  8. (Windows 10 Subsystem for Linux Only)

**Action:** 
Start a Program -> C:\Windows\System32\bash
**Trigger:** 
Daily at midnight
**Settings:** 
Run as soon as a scheduled task is missed -> yes
**Conditions:** 
Start only when any connection is available
Start only if computer is on AC -> no
**General:**
Run only when the user is logged on

