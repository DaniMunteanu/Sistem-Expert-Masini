import json
import firebase_admin
from firebase_admin import credentials, db

class KnowledgeBase:

    def __init__(self):
        #Am citit datele direct din JSON-ul cu datele masinilor. Nu le-am mai citit din tabelul Firebase pentru ca aveam o problema, deci liniile astea comentate sunt deocamdata inutile

        #cred = credentials.Certificate("credentials.json")
        #firebase_admin.initialize_app(cred, {"databaseURL": "https://knowledgebase-fb0c0-default-rtdb.europe-west1.firebasedatabase.app/"})

        self.car_data = {}  #dictionar in care stocam datele din JSON

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

    #Am citit datele direct din JSON-ul cu datele masinilor. Nu le-am mai citit din tabelul Firebase pentru ca aveam o problema, deci metoda asta e deocamdata inutila
    def _update_firebase(self,table_data,path):
        ref = db.reference(path)
        ref.set(table_data)
        print("Data successfully uploaded to Realtime Database!")

    #aici adaugam masinile in dictionar, una cate una
    def _read_table_data(self):
        for car in self._read_file("all-vehicles-model@public.json"):
            new_car = {
                "id":"",
                "vclass":"",
                "fueltype":"",
                "drive":"",
                "trany":"",
                "cylinders":"",
                "make":"",
                "model":""
            }
            new_car["id"] = car["id"]
            new_car["vclass"] = car["vclass"]
            new_car["fueltype"] = car["fueltype"]
            new_car["drive"] = car["drive"]
            new_car["trany"] = car["trany"]
            new_car["cylinders"] = car["cylinders"]
            new_car["make"] = car["make"]
            new_car["model"] = car["model"]

            #field-ul id este unic pentru fiecare masina
            self.car_data.update({int(new_car["id"]) : new_car})

        print(self.car_data.get(21000))   #pentru a afisa masina cu id-ul 21000

kb = KnowledgeBase()
kb._read_table_data()

# Prioritatea verificarilor m-am gandit sa fie vehicle size class -> fuel type -> drive -> transmission -> cylinders -> make