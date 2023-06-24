from Constants import NOTIFICATION_COLLECTION_NAME
from FirebaseConnect import FirebaseConnect
from firebase_admin import firestore

from Models.Notification import Notification


class NotificationService:
    def __init__(self):
        self.db = FirebaseConnect().get_db_reference()

    def get_latest_notification_record(self, notification_type):
        collection_ref = self.db.collection(NOTIFICATION_COLLECTION_NAME)
        query_ref = collection_ref.where("notificationType", "==", notification_type).order_by('created_at',
                                                                                              'DESCENDING').limit(
            1).get()
        if len(query_ref) == 0:
            return None
        notification_dict = query_ref[0].to_dict()
        return Notification(notification_dict['serverRunRecords'], notification_dict['notificationType'])

    def add_notification(self, notification):
        collection_ref = self.db.collection(NOTIFICATION_COLLECTION_NAME)
        data = {
            'serverRunRecords': notification.serverRunRecords,
            'created_at': firestore.firestore.SERVER_TIMESTAMP,
            'notificationType': notification.notificationType
        }
        collection_ref.add(data)
