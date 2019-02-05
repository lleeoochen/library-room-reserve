TODO:
* test chrome drivers for MacOS
* streamline setup process


## Setup
We recommend installing this on csil machines.

  1. Install packages
```
  pip3 install -r requirements.txt --user
```

  2. Add UCSB username and password to env variables (in ~/.bashrc or ~/.bash_profile)
```
  export UMAIL_USERNAME=[Your UCSB Username]
  export UMAIL_PASSWORD=[Your UCSB Password]
```
  3. Run `source ~/.bashrc` or `source ~/.bash_profile` to take changes into effect.

  4. Complete Gmail Authentication flow
```
  python3 do_auth.py --noauth_local_webserver
```
Make sure to sign in with your .edu email!

  5. Use cron to schedule task

  run `crontab -e`  
  type `x 0 * * *  /path/to/python3 /path/to/main.py`  
  replace the `x` in the command with your favorite number from 0-9 (every person in the group should ideally have a different number. it might not make a difference, but better safe than sorry)  
  The file paths may change if you are not running the code on csil

  6. (Windows 10 Subsystem for Linux Only)

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
Hidden -> yes   
Configure for -> Windows 10   

