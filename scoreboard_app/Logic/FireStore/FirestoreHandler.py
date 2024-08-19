#!/usr/local/bin/python3.7
import os
from firebase_admin import credentials, firestore, initialize_app

class FirestoreHandler:
    _app_initialized = False
    
    def __init__(self):
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(script_dir, 'scoreboard-651cf-firebase-adminsdk-obk22-368b90d493.json')

        if not FirestoreHandler._app_initialized:
            cred = credentials.Certificate(self.json_path)
            initialize_app(cred)
            FirestoreHandler._app_initialized = True
    
        self.db = firestore.client()

    def setLiveScoer(self, score_list,collectionName):

        # データをFirestoreから削除
        docs = self.db.collection(collectionName).stream()
        for doc in docs:
            doc.reference.delete()
        
        # データをFirestoreに追加
        for score in score_list:
            self.db.collection(collectionName).add(score)

    def getTeamList(self,collectionName):
        docs = self.db.collection(collectionName).stream()
        score_list = []
        for doc in docs:
            score_list.append(doc.to_dict())
        return score_list