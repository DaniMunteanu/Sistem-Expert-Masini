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
        self.recommendation_limit = 10  # Limitează numărul total de recomandări
        self.recommendation_count = 0   # Contor pentru recomandări
    
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
        print("Searching for cars matching your criteria...")
    
    @Rule(Fact(searching=True),
         Fact(matching_criteria=MATCH.criteria),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype, 
             drive=MATCH.drive, 
             trany=MATCH.trany, 
             cylinders=MATCH.cylinders),
         AS.car << Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            drive=MATCH.drive, 
            trany=MATCH.trany, 
            cylinders=MATCH.cylinders, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def recommend_perfect_match(self, car, id, make, model, year, vclass):
        if self.recommendation_count < self.recommendation_limit:
            self.recommendations.append({
                "id": id,
                "make": make,
                "model": model,
                "year": year,
                "match_level": "Perfect match",
                "vclass": vclass
            })
            self.recommendation_count += 1
            self.retract(car)  # Retrage faptul pentru a evita duplicate
    
    # vclass -> fueltype -> drive -> transmission -> cylinders -> make
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level="Perfect match")),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype, 
             drive=MATCH.drive, 
             trany=MATCH.trany),
         AS.car << Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            drive=MATCH.drive, 
            trany=MATCH.trany, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_cylinders(self, car, id, make, model, year, vclass):
        if self.recommendation_count < self.recommendation_limit:
            self.recommendations.append({
                "id": id,
                "make": make,
                "model": model,
                "year": year,
                "match_level": "Good match (different cylinders)",
                "vclass": vclass
            })
            self.recommendation_count += 1
            self.retract(car)  # Retrage faptul pentru a evita duplicate
        
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level="Perfect match")),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype, 
             drive=MATCH.drive),
         AS.car << Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            drive=MATCH.drive, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_transmission(self, car, id, make, model, year, vclass):
        if self.recommendation_count < self.recommendation_limit:
            self.recommendations.append({
                "id": id,
                "make": make,
                "model": model,
                "year": year,
                "match_level": "Acceptable match (different transmission)",
                "vclass": vclass
            })
            self.recommendation_count += 1
            self.retract(car)  # Retrage faptul pentru a evita duplicate
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level="Perfect match")),
         User(vclass=MATCH.vclass, 
             fueltype=MATCH.fueltype),
         AS.car << Car(vclass=MATCH.vclass, 
            fueltype=MATCH.fueltype, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_drive(self, car, id, make, model, year, vclass):
        if self.recommendation_count < self.recommendation_limit:
            self.recommendations.append({
                "id": id,
                "make": make,
                "model": model,
                "year": year,
                "match_level": "Weaker match (different drive type)",
                "vclass": vclass
            })
            self.recommendation_count += 1
            self.retract(car)  # Retrage faptul pentru a evita duplicate
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level="Perfect match")),
         User(vclass=MATCH.vclass),
         AS.car << Car(vclass=MATCH.vclass, 
            id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year))
    def relax_fuel_type(self, car, id, make, model, year, vclass):
        if self.recommendation_count < self.recommendation_limit:
            self.recommendations.append({
                "id": id,
                "make": make,
                "model": model,
                "year": year,
                "match_level": "Vehicle class match only (different fuel)",
                "vclass": vclass
            })
            self.recommendation_count += 1
            self.retract(car)  # Retrage faptul pentru a evita duplicate
    
    @Rule(Fact(searching=True),
         NOT(Recommendation(match_level="Perfect match")),
         NOT(Recommendation(match_level="Vehicle class match only (different fuel)")),
         AS.car << Car(id=MATCH.id, 
            make=MATCH.make, 
            model=MATCH.model, 
            year=MATCH.year,
            vclass=MATCH.vclass))
    def last_resort(self, car, id, make, model, year, vclass):
        if self.recommendation_count < self.recommendation_limit:
            self.recommendations.append({
                "id": id,
                "make": make,
                "model": model,
                "year": year,
                "match_level": "Last resort recommendation",
                "vclass": vclass
            })
            self.recommendation_count += 1
            self.retract(car)  # Retrage faptul pentru a evita duplicate

    def get_recommendations(self):
        # Sortarea recomandărilor după nivelul de potrivire
        priority_order = {
            "Perfect match": 1,
            "Good match (different cylinders)": 2,
            "Acceptable match (different transmission)": 3,
            "Weaker match (different drive type)": 4,
            "Vehicle class match only (different fuel)": 5,
            "Last resort recommendation": 6
        }
        
        sorted_recommendations = sorted(self.recommendations, 
                                      key=lambda x: priority_order.get(x["match_level"], 999))
        return sorted_recommendations

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
        print("\n=== TOP 3 RECOMMENDATIONS ===\n")
        
        # Afișează cel mult 3 recomandări
        for i, recommendation in enumerate(recommendations[:3], 1):
            car_id = recommendation["id"]
            match_level = recommendation["match_level"]
            car_data = knowledge_base.car_data.get(int(car_id))
            
            print(f"Recommendation #{i} - {match_level}:")
            print(f"Car ID: {car_id}")
            print(f"Make: {car_data['make']}")
            print(f"Model: {car_data['model']}")
            print(f"Year: {car_data['year']}")
            print(f"Vehicle class: {car_data['vclass']}")
            print(f"Fuel type: {car_data['fueltype']}")
            print(f"Drive type: {car_data['drive']}")
            print(f"Transmission: {car_data['trany']}")
            print(f"Cylinders: {car_data['cylinders']}")
            print("-" * 50)
    else:
        print("No recommendations found.")

if __name__ == "__main__":
    kb = KnowledgeBase()
    kb._read_table_data()
    
    run_expert_system(kb)