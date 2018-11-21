TODO:
* use firebase to keep track of reservations
* write optimal scheduling algorithm
* test chrome drivers for MacOS
* figure out how to schedule code to run every 24 hours
* streamline setup process


## Setup
  1. Install Python Selenium package: `sudo pip install -U selenium`
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
