from src import database_access as db
from pprint import pprint
from datetime import datetime
from datetime import time
from datetime import date
import sys


date = date.today()
if len(sys.argv) > 1:
    try:
        date = datetime.strptime(r['date'], "%m/%d/%y")
    except Exception as e:
        sys.exit("Could not parse datestring.\n Correct Usage: python3 check_reservations.py mm/dd/yy")


reservations = db.get_all_reservations()
reservations = list(filter(lambda x: datetime.strptime(x['date'], " %B %d, %Y").date() == date, reservations))

reservations.sort(key=lambda x: datetime.strptime(x['starttime'], "%I:%M%p"))

print("Reservations for " + str(date) + ":")
print("+-------------------------------------------+")
for r in reservations:
    print( "{:7} - {:7}\t{}\t{}".format(r['starttime'], r['endtime'], r['room'], r['user']) )
print("+-------------------------------------------+")
