import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.ApplicationDefault()
app = firebase_admin.initialize_app(cred)
print(app)
db = firestore.client()
