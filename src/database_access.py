import firebase_admin
from firebase_admin import credentials, db
from .constants import FIREBASE_URL, FIREBASE_TOKEN_FILE, FIREBASE_RESERVATIONS
import datetime

# Authenticate Firebase token
cred = credentials.Certificate(FIREBASE_TOKEN_FILE)
firebase_admin.initialize_app(cred, {
	'databaseURL': FIREBASE_URL
})

# Test code
reservations = db.reference(FIREBASE_RESERVATIONS)

def add_reservation(room,date, starttime, endtime, user):
	new_reservation = reservations.push({
	    'room' : room,
		'starttime':starttime,
		'endtime':endtime,
		'date':date,
		'user':user
	})

def get_all_reservations():
	r = reservations.get()
	r = [r[x] for x in r]
	return r

def get_reservations_for(user):
	r = get_all_reservations()
	user_reservations = list(filter(lambda x: x['user'] == user, r))
	return user_reservations


# add_reservation('6969', '420', '1000', '1030', 'yash_rane')
