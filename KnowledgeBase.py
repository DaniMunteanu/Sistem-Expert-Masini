import json
import firebase_admin
from firebase_admin import credentials, db

class KnowledgeBase:
    def __init__(self):
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://knowledgebase-fb0c0-default-rtdb.europe-west1.firebasedatabase.app/"})

    def _read_file(self,file):
        try:
            with open(file) as f:
                data = json.load(f)
                print("succes")
                return data
        except FileNotFoundError:
            print('File not found')
            exit(1)
        except json.JSONDecodeError:
            print('Invalid JSON format')
            exit(1)

    def _update_firebase(self,table_data,path):
        ref = db.reference(path)
        ref.set(table_data)
        print("Data successfully uploaded to Realtime Database!")

# Am rulat deja asta. Datele ar trebui sa fie in https://knowledgebase-fb0c0-default-rtdb.europe-west1.firebasedatabase.app/. Daca nu, trebuie rulata partea asta
kb = KnowledgeBase()
# kb._update_firebase(kb._read_file("all-vehicles-model@public.json"),"/data")

# La fel ca la celalalt apel de _update_firebase
# Prioritatea verificarilor m-am gandit sa fie vehicle size class -> fuel type -> drive -> transmission -> cylinders -> make
# kb._update_firebase(kb._read_file("rules.json"),"/rules")