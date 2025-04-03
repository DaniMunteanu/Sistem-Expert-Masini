import json
from experta import *
from KnowledgeBase import KnowledgeBase



with open("all-vehicles-model@public.json") as f:
    data = json.load(f)

# Afișează valorile unice pentru fiecare câmp
vclass_values = set(car["vclass"] for car in data)
fueltype_values = set(car["fueltype"] for car in data)
drive_values = set(car["drive"] for car in data)
trany_values = set(car["trany"] for car in data)
cylinders_values = set(car["cylinders"] for car in data)

print("Vehicle Classes:", vclass_values)
print("\nFuel Types:", fueltype_values)
print("\nDrive Types:", drive_values)
print("\nTransmission Types:", trany_values)
print("\nCylinder Counts:", cylinders_values)

# Facts that will be used in the system
class User(Fact):
    """User preferences for a car"""
    pass

class Car(Fact):
    """Car information from the knowledge base"""
    pass

class Recommendation(Fact):
    """Recommended car based on user preferences"""
    pass

class CarExpertSystem(KnowledgeEngine):
    def __init__(self, knowledge_base):
        super().__init__()
        self.kb = knowledge_base
        self.recommendations = []
    
    def load_cars(self, car_data):
        for car_id, car_info in car_data.items():
            self.declare(Car(id=car_id, 
                           vclass=car_info["vclass"],
                           fueltype=car_info["fueltype"],
                           drive=car_info["drive"],
                           trany=car_info["trany"],
                           cylinders=car_info["cylinders"],
                           make=car_info["make"],
                           model=car_info["model"],
                           year=car_info["year"]))
    
    @Rule(User(vclass=MATCH.vclass, 
              fueltype=MATCH.fueltype, 
              drive=MATCH.drive, 
              trany=MATCH.trany, 
              cylinders=MATCH.cylinders))
    def match_all_criteria(self, vclass, fueltype, drive, trany, cylinders):
        self.declare(Fact(searching=True, 
                        matching_criteria=["vclass", "fueltype", "drive", "trany", "cylinders"]))
        print("Searching for cars matching all your criteria...")
    
    @Rule(Fact(searching=True),
         Fact(matching_criteria=MATCH.criteria),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype, 
             drive=MATCH.drive, 
             trany=MATCH.trany, 
             cylinders=MATCH.cylinders),
         Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            drive=MATCH.drive, 
            trany=MATCH.trany, 
            cylinders=MATCH.cylinders, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def recommend_perfect_match(self, id, make, model, year, vclass):
        self.declare(Recommendation(id=id, 
                                  make=make, 
                                  model=model, 
                                  year=year, 
                                  match_level="Perfect match",
                                  vclass=vclass))
    
    # vclass -> fueltype -> drive -> transmission -> cylinders -> make
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level="Perfect match")),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype, 
             drive=MATCH.drive, 
             trany=MATCH.trany),
         Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            drive=MATCH.drive, 
            trany=MATCH.trany, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_cylinders(self, id, make, model, year, vclass):
        self.declare(Recommendation(id=id, 
                                  make=make, 
                                  model=model, 
                                  year=year, 
                                  match_level="Good match (different cylinders)",
                                  vclass=vclass))
        
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level=W())),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype, 
             drive=MATCH.drive),
         Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            drive=MATCH.drive, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_transmission(self, id, make, model, year, vclass):
        self.declare(Recommendation(id=id, 
                                  make=make, 
                                  model=model, 
                                  year=year, 
                                  match_level="Acceptable match (different transmission)",
                                  vclass=vclass))
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level=W())),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype),
         Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_drive(self, id, make, model, year, vclass):
        self.declare(Recommendation(id=id, 
                                  make=make, 
                                  model=model, 
                                  year=year, 
                                  match_level="Weaker match (different drive type)",
                                  vclass=vclass))
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level=W())),
         User(vclass=MATCH.vclass),
         Car(vclass=MATCH.vclass, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_fuel_type(self, id, make, model, year, vclass):
        self.declare(Recommendation(id=id, 
                                  make=make, 
                                  model=model, 
                                  year=year, 
                                  match_level="Vehicle class match only (different fuel)",
                                  vclass=vclass))
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level=W())),
         Car(id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year,
            vclass=MATCH.vclass))
    def last_resort(self, id, make, model, year, vclass):
        self.declare(Recommendation(id=id, 
                                  make=make, 
                                  model=model, 
                                  year=year, 
                                  match_level="Last resort recommendation",
                                  vclass=vclass))
                                  
    @Rule(Recommendation(id=MATCH.id, 
                       make=MATCH.make, 
                       model=MATCH.model, 
                       year=MATCH.year, 
                       match_level=MATCH.match_level,
                       vclass=MATCH.vclass))
    def process_recommendation(self, id, make, model, year, match_level, vclass):
        self.recommendations.append({
            "id": id,
            "make": make,
            "model": model,
            "year": year,
            "match_level": match_level,
            "vclass": vclass
        })
        
        print(f"Recommendation - {match_level}:")
        print(f"Car ID: {id}")
        print(f"Make: {make}")
        print(f"Model: {model}")
        print(f"Year: {year}")
        print(f"Vehicle class: {vclass}")
        print("-" * 50)

    def get_recommendations(self):
        return self.recommendations

def run_expert_system(knowledge_base):
    engine = CarExpertSystem(knowledge_base)
    engine.reset()
    engine.load_cars(knowledge_base.car_data)

    vclass = input("Enter preferred vehicle class (e.g., Compact, Midsize, SUV): ")
    fueltype = input("Enter preferred fuel type (e.g., Regular, Premium, Diesel): ")
    drive = input("Enter preferred drive type (e.g., 2-Wheel Drive, 4-Wheel Drive): ")
    trany = input("Enter preferred transmission type (e.g., Automatic, Manual): ")
    cylinders = input("Enter preferred number of cylinders: ")

    engine.declare(User(vclass=vclass, 
                      fueltype=fueltype, 
                      drive=drive, 
                      trany=trany, 
                      cylinders=cylinders))
    

    engine.run()
    recommendations = engine.get_recommendations()
    
    if recommendations:
        top_recommendation = recommendations[0]
        car_id = top_recommendation["id"]

        car_data = knowledge_base.car_data.get(int(car_id))
        print(car_data)
        # print(f"\nDownloading images for the top recommendation (ID: {car_id})...")
        # knowledge_base._download_images(car_data)
    else:
        print("No recommendations found.")

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb._read_table_data()
    run_expert_system(kb)