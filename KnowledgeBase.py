import json
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('AIzaSyAcaYPoAbOiKWRLfFPmQl9WxprGjUaStDI', '62abc5b0b032e4571')

_search_params = {
    'q': 'apple',
    'num': 2,
    'fileType': 'jpg|gif|png',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}

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
                "model":"",
                "year":""
            }
            new_car["id"] = car["id"]
            new_car["vclass"] = car["vclass"]
            new_car["fueltype"] = car["fueltype"]
            new_car["drive"] = car["drive"]
            new_car["trany"] = car["trany"]
            new_car["cylinders"] = car["cylinders"]
            new_car["make"] = car["make"]
            new_car["model"] = car["model"]
            new_car["year"] = car["year"]

            #field-ul id este unic pentru fiecare masina
            self.car_data.update({int(new_car["id"]) : new_car})

        #test_car = self.car_data.get(21000)
        #print(test_car)   #pentru a afisa masina cu id-ul 21000
        
    def _download_images(self,searched_car):
        _search_params["q"] = searched_car["make"] + " " + searched_car["model"] + " " + searched_car["year"] + " " + searched_car["vclass"]
        gis.search(search_params=_search_params, path_to_dir='Images')

kb = KnowledgeBase()
kb._read_table_data()
print(kb.car_data.get(1900))
kb._download_images(kb.car_data.get(1900))

# Prioritatea verificarilor m-am gandit sa fie vehicle size class -> fuel type -> drive -> transmission -> cylinders -> make