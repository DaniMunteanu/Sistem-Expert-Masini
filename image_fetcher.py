import requests

def fetch_image_url(query):
    try:
        api_key = ""
        params = {
            "q": query,
            "tbm": "isch",
            "api_key": api_key
        }
        response = requests.get("https://serpapi.com/search.json", params=params)
        results = response.json()

        if "images_results" in results and results["images_results"]:
            return results["images_results"][0]["original"]
        else:
            return "/cars/default.jpg"
    except Exception as e:
        print(f"[fetch_image_url] Error: {e}")
        return "/cars/default.jpg"
