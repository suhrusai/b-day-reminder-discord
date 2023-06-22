import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from Constants import CERTIFICATE_PATH

class FirebaseConnect:
    _instance = None
    cred = credentials.Certificate(CERTIFICATE_PATH)
    app = firebase_admin.initialize_app(cred)
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def getDbReference(self):
        return firestore.client(self.app)