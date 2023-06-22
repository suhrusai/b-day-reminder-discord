from FirebaseConnect import FirebaseConnect


class Notification():
    def __init__(self,serverRunRecords,notificationType):
        self.serverRunRecords = serverRunRecords
        self.createdAt = None
        self.notificationType = notificationType