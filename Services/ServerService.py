from Constants import SERVERS_COLLECTION_NAME
from FirebaseConnect import FirebaseConnect
from firebase_admin import firestore
from datetime import datetime
from Models.Birthday import Birthday
import re

from Models.Server import Server

def generateServerObject(document):
    documentDict = document.to_dict()
    return Server(
        channelId = documentDict['channelId'],
        channelName= documentDict['channelName'],
        name = documentDict['name'],
        serverId = documentDict['serverId'],
        id = document.id
    )
class ServerService():
    db = FirebaseConnect().getDbReference()
    def getServerById(self,id):
        docRef = self.db.collection(SERVERS_COLLECTION_NAME).document(id)
        document = docRef.get()
        if(document.exists):
            return generateServerObject(document)
        else:
            return None
class ServerCache():
    servers = {}
    serverService = ServerService()
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def presentInCache(self,serverId):
        self.servers.get(serverId) is not None
    def get(self,serverId):
        if self.presentInCache(serverId):
            return self.servers[serverId]
        else:
            self.servers[serverId] = ServerService().getServerById(serverId)
        return self.servers[serverId]
    def add(self,server):
        self.servers[server.id] = server