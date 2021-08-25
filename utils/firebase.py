import pyrebase
import json

class Firebase:

    def __init__(self):
        with open('data/config.json') as d:
            config = json.load(d)
        firebase = pyrebase.initialize_app(config["firebase"])
        self.db = firebase.database()    



    def updateQA(self, data):
        self.db.child("qa").set(data)



    def getQA(self):
        return self.db.child("qa").get().val()