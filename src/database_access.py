import firebase_admin
from firebase_admin import credentials, db
from constants import FIREBASE_URL, FIREBASE_TOKEN_FILE, FIREBASE_RESERVATIONS
import datetime

# Authenticate Firebase token
cred = credentials.Certificate(FIREBASE_TOKEN_FILE)
firebase_admin.initialize_app(cred, {
	'databaseURL': FIREBASE_URL
})

# Test code
reservations = db.reference(FIREBASE_RESERVATIONS)
new_reservation = reservations.push({
    'room' : 2137,
    'time' : 15.0
})
