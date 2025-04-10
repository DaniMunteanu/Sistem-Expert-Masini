from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import List, Union
from Inference import CarExpert
from image_fetcher import fetch_image_url


router = APIRouter()

class PreferenceRequest(BaseModel):
    vclass: List[str]
    fueltype: List[str]
    drive: List[str]
    trany: List[str]
    cylinders: List[Union[str, int]]


@router.post("/recommend")
async def recommend(preferences: PreferenceRequest):
    expert = CarExpert()
    user_preferences = preferences.dict()
    print("Preferences received:", user_preferences)

    for key in user_preferences:
        val = user_preferences[key]
        if isinstance(val, list) and not val:
            raise HTTPException(status_code=400, detail=f"Missing selection for field: {key}")

    for key in ["vclass", "fueltype", "drive", "trany"]:
        user_preferences[key] = [str(v).strip() for v in user_preferences[key]]

    normalized_cylinders = []
    for v in user_preferences["cylinders"]:
        try:
            normalized_cylinders.append(int(v))
        except (ValueError, TypeError):
            normalized_cylinders.append(str(v).strip())
    user_preferences["cylinders"] = normalized_cylinders

    results = expert.backward_chain("find_best_recommendations", user_preferences)

    priority_order = {
        "Perfect match": 1,
        "Good match (different cylinders)": 2,
        "Acceptable match (different transmission)": 3,
        "Weaker match (different drive type)": 4,
        "Vehicle class match only (different fuel)": 5,
        "Last resort recommendation": 6
    }

    sorted_results = sorted(results, key=lambda x: priority_order.get(x["match_level"], 999))

    def get_image_url(make, model):
        return fetch_image_url(f"{make} {model} car")



    return {
        "recommendations": [
            {
                "id": r["id"],
                "make": r["car_data"].get("make"),
                "model": r["car_data"].get("model"),
                "year": r["car_data"].get("year"),
                "match_level": r["match_level"],
                "vclass": r["car_data"].get("vclass"),
                "fueltype": r["car_data"].get("fueltype"),
                "drive": r["car_data"].get("drive"),
                "trany": r["car_data"].get("trany"),
                "cylinders": r["car_data"].get("cylinders"),
                "image": get_image_url(r["car_data"].get("make"), r["car_data"].get("model"))
            }
            for r in sorted_results[:3]
        ]
    }


@router.post("/options/filter/{field}")
async def get_filtered_options(field: str, body: dict = Body(...)):
    expert = CarExpert()
    print(f"Requested dynamic options for field: '{field}'")
    print(f"Filters received: {body}")

    filtered = expert.car_data

    for key, value in body.items():
        if value:
            if isinstance(value, list):
                filtered = [car for car in filtered if car.get(key) in value]
            else:
                filtered = [car for car in filtered if car.get(key) == value]

    print(f"Matching vehicles after filtering: {len(filtered)}")

    values = set(car.get(field) for car in filtered if car.get(field) is not None)

    if not values:
        print("No values found after filtering — fallback to full dataset.")
        values = set(car.get(field) for car in expert.car_data if car.get(field) is not None)

    grouped = expert.group_options(values, field)

    result = []
    for group_label, group_values in grouped.items():
        result.append({
            "label": group_label,
            "values": group_values
        })

    return {"options": result}
