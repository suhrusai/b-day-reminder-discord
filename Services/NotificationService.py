from Constants import NOTIFICATION_COLLECTION_NAME
from FirebaseConnect import FirebaseConnect
from firebase_admin import firestore

from Models.Notification import Notification
class NotificationService():
    def __init__(self):
        self.db = FirebaseConnect().getDbReference()
    def getLatestNotificationRecord(self,notificationType):
        collection_ref = self.db.collection(NOTIFICATION_COLLECTION_NAME)
        query_ref = collection_ref.where("notificationType","==",notificationType).order_by('created_at','DESCENDING').limit(1).get()
        if(len(query_ref) == 0):
            return None
        notificationDict= query_ref[0].to_dict()
        return Notification(notificationDict['serverRunRecords'],notificationDict['notificationType'])
    def addNotification(self,notification):

        collection_ref = self.db.collection(NOTIFICATION_COLLECTION_NAME)
        data = {
            'serverRunRecords' : notification.serverRunRecords,
            'created_at' : firestore.firestore.SERVER_TIMESTAMP,
            'notificationType': notification.notificationType
        }
        collection_ref.add(data)


