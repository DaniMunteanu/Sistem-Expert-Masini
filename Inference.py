import json

class CarExpert:
    def __init__(self, knowledge_base_file="all-vehicles-model@public.json"):
        self.load_knowledge_base(knowledge_base_file)
        self.recommendations = []
        self.recommendation_limit = 10
        
    def load_knowledge_base(self, knowledge_base_file):
        """Loads the knowledge base from the JSON file"""
        try:
            with open(knowledge_base_file) as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.car_data = [car_info for car_id, car_info in data.items()]
                else:
                    self.car_data = data
            print(f"Knowledge base successfully loaded: {len(self.car_data)} vehicles")
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            self.car_data = []
            
    def display_available_options(self):
        """Display available options for each criterion"""
        if not self.car_data:
            print("Knowledge base has not been loaded.")
            return
            
        vclass_values = set(car.get("vclass") for car in self.car_data if car.get("vclass") is not None)
        fueltype_values = set(car.get("fueltype") for car in self.car_data if car.get("fueltype") is not None)
        drive_values = set(car.get("drive") for car in self.car_data if car.get("drive") is not None)
        trany_values = set(car.get("trany") for car in self.car_data if car.get("trany") is not None)
        cylinders_values = set(car.get("cylinders") for car in self.car_data if car.get("cylinders") is not None)

        print("Available vehicle classes:", sorted(list(vclass_values)))
        print("Available fuel types:", sorted(list(fueltype_values)))
        print("Available drive types:", sorted(list(drive_values)))
        print("Available transmission types:", sorted(list(trany_values)))
        print("Available cylinder counts:", sorted(list(cylinders_values), key=str))
    
    def get_user_preferences(self):
        """Gets user preferences interactively, showing available options at each step"""
        print("\n=== Enter your preferences ===")
        user_prefs = {}
        
        # Step 1: Choose vehicle class
        vclass_values = sorted(list(set(car.get("vclass") for car in self.car_data 
                                  if car.get("vclass") is not None)))
        print("\nAvailable vehicle classes:")
        for i, vclass in enumerate(vclass_values, 1):
            print(f"{i}. {vclass}")
        
        choice = input("\nSelect vehicle class (enter number or type custom value): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(vclass_values):
                user_prefs["vclass"] = vclass_values[index]
            else:
                user_prefs["vclass"] = choice
        except ValueError:
            user_prefs["vclass"] = choice
            
        # Filter cars based on vehicle class
        filtered_cars = [car for car in self.car_data if car.get("vclass") == user_prefs["vclass"]]
        
        # Step 2: Choose fuel type
        fueltype_values = sorted(list(set(car.get("fueltype") for car in filtered_cars 
                                    if car.get("fueltype") is not None)))
        print("\nAvailable fuel types for selected vehicle class:")
        for i, fueltype in enumerate(fueltype_values, 1):
            print(f"{i}. {fueltype}")
            
        choice = input("\nSelect fuel type (enter number or type custom value): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(fueltype_values):
                user_prefs["fueltype"] = fueltype_values[index]
            else:
                user_prefs["fueltype"] = choice
        except ValueError:
            user_prefs["fueltype"] = choice
            
        # Filter cars based on fuel type
        filtered_cars = [car for car in filtered_cars 
                        if car.get("fueltype") == user_prefs["fueltype"]]
        
        # Step 3: Choose drive type
        drive_values = sorted(list(set(car.get("drive") for car in filtered_cars 
                                 if car.get("drive") is not None)))
        print("\nAvailable drive types for selected options:")
        for i, drive in enumerate(drive_values, 1):
            print(f"{i}. {drive}")
            
        choice = input("\nSelect drive type (enter number or type custom value): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(drive_values):
                user_prefs["drive"] = drive_values[index]
            else:
                user_prefs["drive"] = choice
        except ValueError:
            user_prefs["drive"] = choice
            
        # Filter cars based on drive type
        filtered_cars = [car for car in filtered_cars 
                        if car.get("drive") == user_prefs["drive"]]
        
        # Step 4: Choose transmission type
        trany_values = sorted(list(set(car.get("trany") for car in filtered_cars 
                                 if car.get("trany") is not None)))
        print("\nAvailable transmission types for selected options:")
        for i, trany in enumerate(trany_values, 1):
            print(f"{i}. {trany}")
            
        choice = input("\nSelect transmission type (enter number or type custom value): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(trany_values):
                user_prefs["trany"] = trany_values[index]
            else:
                user_prefs["trany"] = choice
        except ValueError:
            user_prefs["trany"] = choice
            
        # Filter cars based on transmission type
        filtered_cars = [car for car in filtered_cars 
                        if car.get("trany") == user_prefs["trany"]]
        
        # Step 5: Choose cylinders
        cylinders_values = sorted(list(set(car.get("cylinders") for car in filtered_cars 
                                    if car.get("cylinders") is not None)), key=str)
        print("\nAvailable cylinder counts for selected options:")
        for i, cylinders in enumerate(cylinders_values, 1):
            print(f"{i}. {cylinders}")
            
        choice = input("\nSelect cylinders (enter number or type custom value): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(cylinders_values):
                user_prefs["cylinders"] = cylinders_values[index]
            else:
                user_prefs["cylinders"] = choice
        except ValueError:
            user_prefs["cylinders"] = choice
            
        print("\n=== Your preferences ===")
        print(f"Vehicle class: {user_prefs['vclass']}")
        print(f"Fuel type: {user_prefs['fueltype']}")
        print(f"Drive type: {user_prefs['drive']}")
        print(f"Transmission: {user_prefs['trany']}")
        print(f"Cylinders: {user_prefs['cylinders']}")
        
        return user_prefs
    
    def backward_chain(self, goal, user_preferences):
        self.recommendations = []
        models_already_recommended = set()
        
        # Rule hierarchy: from most specific to most general
        rule_hierarchy = [
            self.rule_perfect_match,
            self.rule_relax_cylinders,
            self.rule_relax_transmission,
            self.rule_relax_drive,
            self.rule_relax_fuel_type,
            self.rule_last_resort
        ]
        
        # Try each rule in order
        for rule in rule_hierarchy:
            if len(self.recommendations) >= self.recommendation_limit:
                break
            potential_matches = rule(user_preferences)
            
            for match in potential_matches:
                make = match["car_data"].get("make")
                model = match["car_data"].get("model")
                model_key = f"{make}_{model}"

                if model_key not in models_already_recommended:
                    self.recommendations.append(match)
                    models_already_recommended.add(model_key)

                    if len(self.recommendations) >= self.recommendation_limit:
                        break
            if len(self.recommendations) > 0 and goal == "find_any_recommendation":
                break
                
        return self.recommendations
    
    def rule_perfect_match(self, user_prefs):
        """Rule for perfect match"""
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") == user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") == user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") == user_prefs["drive"] and user_prefs["drive"] and
                car.get("trany") == user_prefs["trany"] and user_prefs["trany"] and
                car.get("cylinders") == user_prefs["cylinders"] and user_prefs["cylinders"]):
                
                matches.append({
                    "id": car_id,
                    "make": car.get("make", "Unknown"),
                    "model": car.get("model", "Unknown"),
                    "year": car.get("year", "Unknown"),
                    "match_level": "Perfect match",
                    "car_data": car
                })
        
        return matches
    
    def rule_relax_cylinders(self, user_prefs):
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") == user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") == user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") == user_prefs["drive"] and user_prefs["drive"] and
                car.get("trany") == user_prefs["trany"] and user_prefs["trany"] and
                car.get("cylinders") is not None and
                user_prefs["cylinders"] and
                car.get("cylinders") != user_prefs["cylinders"]):
                
                matches.append({
                    "id": car_id,
                    "make": car.get("make", "Unknown"),
                    "model": car.get("model", "Unknown"),
                    "year": car.get("year", "Unknown"),
                    "match_level": "Good match (different cylinders)",
                    "car_data": car
                })
        
        return matches
    
    def rule_relax_transmission(self, user_prefs):
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") == user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") == user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") == user_prefs["drive"] and user_prefs["drive"] and
                car.get("trany") is not None and
                user_prefs["trany"] and
                car.get("trany") != user_prefs["trany"]):
                
                matches.append({
                    "id": car_id,
                    "make": car.get("make", "Unknown"),
                    "model": car.get("model", "Unknown"),
                    "year": car.get("year", "Unknown"),
                    "match_level": "Acceptable match (different transmission)",
                    "car_data": car
                })
        
        return matches
    
    def rule_relax_drive(self, user_prefs):
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") == user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") == user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") is not None and
                user_prefs["drive"] and
                car.get("drive") != user_prefs["drive"]):
                
                matches.append({
                    "id": car_id,
                    "make": car.get("make", "Unknown"),
                    "model": car.get("model", "Unknown"),
                    "year": car.get("year", "Unknown"),
                    "match_level": "Weaker match (different drive type)",
                    "car_data": car
                })
        
        return matches
    
    def rule_relax_fuel_type(self, user_prefs):
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") == user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") is not None and
                user_prefs["fueltype"] and
                car.get("fueltype") != user_prefs["fueltype"]):
                
                matches.append({
                    "id": car_id,
                    "make": car.get("make", "Unknown"),
                    "model": car.get("model", "Unknown"),
                    "year": car.get("year", "Unknown"),
                    "match_level": "Vehicle class match only (different fuel)",
                    "car_data": car
                })
        
        return matches
    
    def rule_last_resort(self, user_prefs):
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") is not None and
                user_prefs["vclass"] and
                car.get("vclass") != user_prefs["vclass"]):
                
                matches.append({
                    "id": car_id,
                    "make": car.get("make", "Unknown"),
                    "model": car.get("model", "Unknown"),
                    "year": car.get("year", "Unknown"),
                    "match_level": "Last resort recommendation",
                    "car_data": car
                })
        
        return matches
    
    def display_recommendations(self, recommendations, limit=3):
        if not recommendations:
            print("\nNo recommendations found that match your preferences.")
            return
            
        print(f"\n=== TOP {min(limit, len(recommendations))} RECOMMENDATIONS ===\n")
        
        for i, recommendation in enumerate(recommendations[:limit], 1):
            car_data = recommendation["car_data"]
            match_level = recommendation["match_level"]
            
            print(f"Recommendation #{i} - {match_level}:")
            print(f"Make: {car_data.get('make', 'Unknown')}")
            print(f"Model: {car_data.get('model', 'Unknown')}")
            print(f"Year: {car_data.get('year', 'Unknown')}")
            print(f"Vehicle class: {car_data.get('vclass', 'Unknown')}")
            print(f"Fuel type: {car_data.get('fueltype', 'Unknown')}")
            print(f"Drive type: {car_data.get('drive', 'Unknown')}")
            print(f"Transmission: {car_data.get('trany', 'Unknown')}")
            print(f"Cylinders: {car_data.get('cylinders', 'Unknown')}")
            print("-" * 50)
            
    def run(self):        
        user_preferences = self.get_user_preferences()
        recommendations = self.backward_chain("find_best_recommendations", user_preferences)
        
        # Sort recommendations by match level
        priority_order = {
            "Perfect match": 1,
            "Good match (different cylinders)": 2,
            "Acceptable match (different transmission)": 3,
            "Weaker match (different drive type)": 4,
            "Vehicle class match only (different fuel)": 5,
            "Last resort recommendation": 6
        }
        
        sorted_recommendations = sorted(recommendations, 
                                      key=lambda x: priority_order.get(x["match_level"], 999))
        
        self.display_recommendations(sorted_recommendations)


if __name__ == "__main__":
    expert_system = CarExpert()
    expert_system.run()