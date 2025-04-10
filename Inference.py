import json
import os
from google_images_search import GoogleImagesSearch

# Google API KEY ---------|
#                         V
gis = GoogleImagesSearch('', '62abc5b0b032e4571')

_search_params = {
    'q': '',
    'num': 2,
    'fileType': 'jpg',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}

class CarExpert:
    def __init__(self, knowledge_base_file="all-vehicles-model@public.json"):
        self.load_knowledge_base(knowledge_base_file)
        self.recommendations = []
        self.recommendation_limit = 10
        
    def load_knowledge_base(self, knowledge_base_file):
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

    def _download_images(self,searched_car):
        _search_params["q"] = searched_car["make"] + " " + searched_car["model"] + " " + searched_car["year"]
        
        gis.search(search_params=_search_params, path_to_dir='Images', custom_image_name = searched_car["make"] + "_" + searched_car["model"] + "_" + searched_car["year"])
    
    def group_options(self, options, option_type):
        if option_type == "vclass":
            grouped = {}
            for option in options:
                if "Sport Utility Vehicle" in option or "SUV" in option:
                    grouped.setdefault("SUV", []).append(option)
                elif "Pickup" in option:
                    grouped.setdefault("Pickup Truck", []).append(option)
                elif "Cars" in option or "Compact" in option or "Subcompact" in option or "Minicompact" in option:
                    grouped.setdefault("Car", []).append(option)
                elif "Station Wagon" in option:
                    grouped.setdefault("Station Wagon", []).append(option)
                elif "Van" in option:
                    grouped.setdefault("Van", []).append(option)
                elif "Two Seaters" in option:
                    grouped.setdefault("Sports Car", []).append(option)
                elif "Special Purpose" in option:
                    grouped.setdefault("Special Purpose", []).append(option)
                else:
                    grouped.setdefault("Other", []).append(option)
            return grouped
            
        elif option_type == "fueltype":
            grouped = {}
            for option in options:
                if option is None:
                    continue
                if "Regular" in option or "Gasoline" in option or "Gas" in option:
                    grouped.setdefault("Gasoline", []).append(option)
                elif "Premium" in option:
                    grouped.setdefault("Premium Gasoline", []).append(option)
                elif "Diesel" in option:
                    grouped.setdefault("Diesel", []).append(option)
                elif "Electric" in option or "Electricity" in option:
                    grouped.setdefault("Electric/Hybrid", []).append(option)
                elif "CNG" in option or "natural gas" in option:
                    grouped.setdefault("Natural Gas", []).append(option)
                elif "Hydrogen" in option:
                    grouped.setdefault("Hydrogen", []).append(option)
                else:
                    grouped.setdefault("Other", []).append(option)
            return grouped
            
        elif option_type == "drive":
            grouped = {}
            for option in options:
                if option is None:
                    continue
                if "All-Wheel" in option:
                    grouped.setdefault("All-Wheel Drive", []).append(option)
                elif "4-Wheel" in option:
                    grouped.setdefault("4-Wheel Drive", []).append(option)
                elif "Front-Wheel" in option:
                    grouped.setdefault("Front-Wheel Drive", []).append(option)
                elif "Rear-Wheel" in option:
                    grouped.setdefault("Rear-Wheel Drive", []).append(option)
                elif "2-Wheel" in option:
                    grouped.setdefault("2-Wheel Drive", []).append(option)
                else:
                    grouped.setdefault("Other", []).append(option)
            return grouped
            
        elif option_type == "trany":
            grouped = {}
            for option in options:
                if option is None:
                    continue
                if "Automatic" in option:
                    grouped.setdefault("Automatic", []).append(option)
                elif "Manual" in option:
                    grouped.setdefault("Manual", []).append(option)
                else:
                    grouped.setdefault("Other", []).append(option)
            return grouped
            
        elif option_type == "cylinders":
            grouped = {}
            for option in options:
                if option is None:
                    continue
                option_str = str(option)
                if option_str in ["2", "3"]:
                    grouped.setdefault("Small (2-3)", []).append(option)
                elif option_str == "4":
                    grouped.setdefault("4 Cylinders", []).append(option)
                elif option_str in ["5", "6"]:
                    grouped.setdefault("Medium (5-6)", []).append(option)
                elif option_str in ["8", "10", "12", "16"]:
                    grouped.setdefault("Large (8+)", []).append(option)
                else:
                    grouped.setdefault("Other", []).append(option)
            return grouped
            
        # Default - fara grupare
        return {option: [option] for option in options}
            
    def display_available_options(self):
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
        user_prefs = {}
        
        vclass_values = sorted(list(set(car.get("vclass") for car in self.car_data 
                                  if car.get("vclass") is not None)))
        grouped_vclass = self.group_options(vclass_values, "vclass")
        
        print("\nAvailable vehicle classes:")
        for i, (group_name, options) in enumerate(grouped_vclass.items(), 1):
            print(f"{i}. {group_name}")
        
        choice = input("\nSelect vehicle class type (enter number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(grouped_vclass):
                group_name = list(grouped_vclass.keys())[index]

                options = grouped_vclass[group_name]
                if len(options) > 1:
                    print(f"\nSpecific options for {group_name}:")
                    for j, option in enumerate(options, 1):
                        print(f"{j}. {option}")
                    sub_choice = input("\nSelect specific option (enter number or 0 for any): ")
                    try:
                        sub_index = int(sub_choice) - 1
                        if sub_index == -1:
                            user_prefs["vclass"] = options[0]
                            print(f"Selected: Any {group_name}")
                        elif 0 <= sub_index < len(options):
                            user_prefs["vclass"] = options[sub_index]
                            print(f"Selected: {options[sub_index]}")
                        else:
                            user_prefs["vclass"] = options[0]
                            print(f"Invalid choice. Selected: {options[0]}")
                    except ValueError:
                        user_prefs["vclass"] = options[0]
                        print(f"Invalid choice. Selected: {options[0]}")
                else:
                    user_prefs["vclass"] = options[0]
                    print(f"Selected: {options[0]}")
            else:
                custom_vclass = input("Enter custom vehicle class: ")
                user_prefs["vclass"] = custom_vclass
                print(f"Selected: {custom_vclass}")
        except ValueError:
            user_prefs["vclass"] = choice
            print(f"Selected: {choice}")

        filtered_cars = [car for car in self.car_data if car.get("vclass") in user_prefs["vclass"]]

        fueltype_values = sorted(list(set(car.get("fueltype") for car in filtered_cars 
                                    if car.get("fueltype") is not None)))

        if not fueltype_values:
            fueltype_values = sorted(list(set(car.get("fueltype") for car in self.car_data 
                                      if car.get("fueltype") is not None)))
        
        grouped_fueltype = self.group_options(fueltype_values, "fueltype")
        
        print("\nAvailable fuel types:")
        for i, (group_name, options) in enumerate(grouped_fueltype.items(), 1):
            print(f"{i}. {group_name}")
            
        choice = input("\nSelect fuel type (enter number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(grouped_fueltype):
                group_name = list(grouped_fueltype.keys())[index]

                options = grouped_fueltype[group_name]
                if len(options) > 1:
                    print(f"\nSpecific options for {group_name}:")
                    for j, option in enumerate(options, 1):
                        print(f"{j}. {option}")
                    sub_choice = input("\nSelect specific option (enter number or 0 for any): ")
                    try:
                        sub_index = int(sub_choice) - 1
                        if sub_index == -1:
                            user_prefs["fueltype"] = options[0]
                            print(f"Selected: Any {group_name}")
                        elif 0 <= sub_index < len(options):
                            user_prefs["fueltype"] = options[sub_index]
                            print(f"Selected: {options[sub_index]}")
                        else:
                            user_prefs["fueltype"] = options[0]
                            print(f"Invalid choice. Selected: {options[0]}")
                    except ValueError:
                        user_prefs["fueltype"] = options[0]
                        print(f"Invalid choice. Selected: {options[0]}")
                else:
                    user_prefs["fueltype"] = options[0]
                    print(f"Selected: {options[0]}")
            else:
                custom_fueltype = input("Enter custom fuel type: ")
                user_prefs["fueltype"] = custom_fueltype
                print(f"Selected: {custom_fueltype}")
        except ValueError:
            user_prefs["fueltype"] = choice
            print(f"Selected: {choice}")

        filtered_cars = [car for car in filtered_cars 
                        if car.get("fueltype") in user_prefs["fueltype"]]

        drive_values = sorted(list(set(car.get("drive") for car in filtered_cars 
                                 if car.get("drive") is not None)))

        if not drive_values:
            drive_values = sorted(list(set(car.get("drive") for car in self.car_data 
                                   if car.get("drive") is not None)))
        
        grouped_drive = self.group_options(drive_values, "drive")
        
        print("\nAvailable drive types:")
        for i, (group_name, options) in enumerate(grouped_drive.items(), 1):
            print(f"{i}. {group_name}")
            
        choice = input("\nSelect drive type (enter number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(grouped_drive):
                group_name = list(grouped_drive.keys())[index]
            
                options = grouped_drive[group_name]
                if len(options) > 1:
                    print(f"\nSpecific options for {group_name}:")
                    for j, option in enumerate(options, 1):
                        print(f"{j}. {option}")
                    sub_choice = input("\nSelect specific option (enter number or 0 for any): ")
                    try:
                        sub_index = int(sub_choice) - 1
                        if sub_index == -1:
                            user_prefs["drive"] = options[0]
                            print(f"Selected: Any {group_name}")
                        elif 0 <= sub_index < len(options):
                            user_prefs["drive"] = options[sub_index]
                            print(f"Selected: {options[sub_index]}")
                        else:
                            user_prefs["drive"] = options[0]
                            print(f"Invalid choice. Selected: {options[0]}")
                    except ValueError:
                        user_prefs["drive"] = options[0]
                        print(f"Invalid choice. Selected: {options[0]}")
                else:
                    user_prefs["drive"] = options[0]
                    print(f"Selected: {options[0]}")
            else:
                custom_drive = input("Enter custom drive type: ")
                user_prefs["drive"] = custom_drive
                print(f"Selected: {custom_drive}")
        except ValueError:
            user_prefs["drive"] = choice
            print(f"Selected: {choice}")
            
        filtered_cars = [car for car in filtered_cars 
                        if car.get("drive") in user_prefs["drive"]]
        
        trany_values = sorted(list(set(car.get("trany") for car in filtered_cars 
                                 if car.get("trany") is not None)))
        
        if not trany_values:
            trany_values = sorted(list(set(car.get("trany") for car in self.car_data 
                                   if car.get("trany") is not None)))
        
        grouped_trany = self.group_options(trany_values, "trany")
        
        print("\nAvailable transmission types:")
        for i, (group_name, options) in enumerate(grouped_trany.items(), 1):
            print(f"{i}. {group_name}")
            
        choice = input("\nSelect transmission type (enter number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(grouped_trany):
                group_name = list(grouped_trany.keys())[index]
                
                options = grouped_trany[group_name]
                if len(options) > 1:
                    print(f"\nSpecific options for {group_name}:")
                    for j, option in enumerate(options, 1):
                        print(f"{j}. {option}")
                    sub_choice = input("\nSelect specific option (enter number or 0 for any): ")
                    try:
                        sub_index = int(sub_choice) - 1
                        if sub_index == -1:
                            user_prefs["trany"] = options[0]
                            print(f"Selected: Any {group_name}")
                        elif 0 <= sub_index < len(options):
                            user_prefs["trany"] = options[sub_index]
                            print(f"Selected: {options[sub_index]}")
                        else:
                            user_prefs["trany"] = options[0]
                            print(f"Invalid choice. Selected: {options[0]}")
                    except ValueError:
                        user_prefs["trany"] = options[0]
                        print(f"Invalid choice. Selected: {options[0]}")
                else:
                    user_prefs["trany"] = options[0]
                    print(f"Selected: {options[0]}")
            else:
                custom_trany = input("Enter custom transmission type: ")
                user_prefs["trany"] = custom_trany
                print(f"Selected: {custom_trany}")
        except ValueError:
            user_prefs["trany"] = choice
            print(f"Selected: {choice}")
            
        filtered_cars = [car for car in filtered_cars 
                        if car.get("trany") in user_prefs["trany"]]
        
        cylinders_values = sorted(list(set(car.get("cylinders") for car in filtered_cars 
                                    if car.get("cylinders") is not None)), key=str)
        
        if not cylinders_values:
            cylinders_values = sorted(list(set(car.get("cylinders") for car in self.car_data 
                                      if car.get("cylinders") is not None)), key=str)
        
        grouped_cylinders = self.group_options(cylinders_values, "cylinders")
        
        print("\nAvailable cylinder counts:")
        for i, (group_name, options) in enumerate(grouped_cylinders.items(), 1):
            print(f"{i}. {group_name}")
            
        choice = input("\nSelect cylinder count (enter number): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(grouped_cylinders):
                group_name = list(grouped_cylinders.keys())[index]
                
                options = grouped_cylinders[group_name]
                if len(options) > 1:
                    print(f"\nSpecific options for {group_name}:")
                    for j, option in enumerate(options, 1):
                        print(f"{j}. {option}")
                    sub_choice = input("\nSelect specific option (enter number or 0 for any): ")
                    try:
                        sub_index = int(sub_choice) - 1
                        if sub_index == -1:
                            user_prefs["cylinders"] = options[0]
                            print(f"Selected: Any {group_name}")
                        elif 0 <= sub_index < len(options):
                            user_prefs["cylinders"] = options[sub_index]
                            print(f"Selected: {options[sub_index]}")
                        else:
                            user_prefs["cylinders"] = options[0]
                            print(f"Invalid choice. Selected: {options[0]}")
                    except ValueError:
                        user_prefs["cylinders"] = options[0]
                        print(f"Invalid choice. Selected: {options[0]}")
                else:
                    user_prefs["cylinders"] = options[0]
                    print(f"Selected: {options[0]}")
            else:
                custom_cylinders = input("Enter custom cylinder count: ")
                user_prefs["cylinders"] = custom_cylinders
                print(f"Selected: {custom_cylinders}")
        except ValueError:
            user_prefs["cylinders"] = choice
            print(f"Selected: {choice}")
            
        print("\n=== Your preferences ===")
        print(f"Vehicle class: {user_prefs['vclass']}")
        print(f"Fuel type: {user_prefs['fueltype']}")
        print(f"Drive type: {user_prefs['drive']}")
        print(f"Transmission: {user_prefs['trany']}")
        print(f"Cylinders: {user_prefs['cylinders']}")
        
        return user_prefs
    
    def rule_perfect_match(self, user_prefs):
        matches = []
        for car_id, car in enumerate(self.car_data):
            if (car.get("vclass") in user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") in user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") in user_prefs["drive"] and user_prefs["drive"] and
                car.get("trany") in user_prefs["trany"] and user_prefs["trany"] and
                car.get("cylinders") in user_prefs["cylinders"] and user_prefs["cylinders"]):
                
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
            if (car.get("vclass") in user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") in user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") in user_prefs["drive"] and user_prefs["drive"] and
                car.get("trany") in user_prefs["trany"] and user_prefs["trany"] and
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
            if (car.get("vclass") in user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") in user_prefs["fueltype"] and user_prefs["fueltype"] and
                car.get("drive") in user_prefs["drive"] and user_prefs["drive"] and
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
            if (car.get("vclass") in user_prefs["vclass"] and user_prefs["vclass"] and
                car.get("fueltype") in user_prefs["fueltype"] and user_prefs["fueltype"] and
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
            if (car.get("vclass") in user_prefs["vclass"] and user_prefs["vclass"] and
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
    
    def backward_chain(self, goal, user_preferences):
        self.recommendations = []
        models_already_recommended = set() # Salvare modele deja recomandate
        
        rule_hierarchy = [
            self.rule_perfect_match,
            self.rule_relax_cylinders,
            self.rule_relax_transmission,
            self.rule_relax_drive,
            self.rule_relax_fuel_type,
            self.rule_last_resort
        ]
        
        # Incearca fiecare regula pe rand
        for rule in rule_hierarchy:
            if len(self.recommendations) >= self.recommendation_limit:
                break
        
            potential_matches = rule(user_preferences)
            
            for match in potential_matches:
                make = match["car_data"].get("make")
                model = match["car_data"].get("model")
                model_key = f"{make}_{model}"
                
                # Verificare recomandare dubla
                if model_key not in models_already_recommended:
                    self.recommendations.append(match)
                    models_already_recommended.add(model_key)
                
                    if len(self.recommendations) >= self.recommendation_limit:
                        break
            
            # Oprire cand ajunge la 3 recomandari
            if len(self.recommendations) > 0 and goal == "find_any_recommendation":
                break
                
        return self.recommendations
    
    def display_recommendations(self, recommendations, limit=3):
        if not recommendations:
            print("\nNo recommendations found that match your preferences.")
            return
            
        # Sterg pozele recomandarilor trecute    
        folder_path = 'Images'

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

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

            # Descarc pozele recomandarilor curente
            self._download_images(car_data)
            print("-" * 50)

    def run(self):        
        user_preferences = self.get_user_preferences()
    
        recommendations = self.backward_chain("find_best_recommendations", user_preferences)
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