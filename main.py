from src import reserve_room, email_confirmation
import time
import sys

if len(sys.argv) > 1:
    print("initial imports are working correctly!")
else:
    num_picked = reserve_room.main()
    print("Reserving " + str(num_picked) + " rooms")
    num_picked = 7
    for i in range(num_picked):
        email_confirmation.main()
        time.sleep(5)
