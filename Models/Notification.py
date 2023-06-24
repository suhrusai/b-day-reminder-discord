from FirebaseConnect import FirebaseConnect


class Notification:
    def __init__(self, server_run_records, notification_type):
        self.serverRunRecords = server_run_records
        self.createdAt = None
        self.notificationType = notification_type
