from Constants import SERVER_RUN_RECORD_COLLECTION_NAME
from FirebaseConnect import FirebaseConnect
from Models.ServerRunRecord import ServerRunRecord
from firebase_admin import firestore
def generateServerRunRecord(document):
    documentDict = document.to_dict()
    return ServerRunRecord(
        server_id= documentDict['serverId'],
        message_ids= documentDict['messageIds'],
        birthday_ids= documentDict['birthdayIds']
    )
class ServerRunRecordService():
    def __init__(self):
        self.db = FirebaseConnect().get_db_reference()
    def getServerRunRecordById(self,id):
        docRef = self.db.collection(SERVER_RUN_RECORD_COLLECTION_NAME).document(id)
        document = docRef.get()
        if (document.exists): 
            return generateServerRunRecord(document)
        return None 
    def addServerRunRecord(self,serverRunRecord):
        collection_ref = self.db.collection(SERVER_RUN_RECORD_COLLECTION_NAME)
        data = {
            'serverId': serverRunRecord.serverId,
            'messageIds': serverRunRecord.messageIds,
            'birthdayIds': serverRunRecord.birthdayIds,
        }
        doc_ref = collection_ref.add(data)[1]
        print('Document written with ID: ', doc_ref.id)
        return doc_ref.id