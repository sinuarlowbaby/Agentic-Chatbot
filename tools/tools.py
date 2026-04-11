from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import requests
load_dotenv()

@tool(name="get_weather", description="Get the weather data for a given city")
def get_weather(city_name: str) -> str:
    geo_url = f"https://open-meteo.com{city_name}&count=1&language=en&format=json"
    geo_resp = requests.get(geo_url).json()
    
    if not geo_resp.get('results'):
        return f"City '{city_name}' not found."
    
    # Extract location details
    location = geo_resp['results'][0]
    lat, lon = location['latitude'], location['longitude']
    full_name = f"{location['name']}, {location.get('country', '')}"
    
    # 2. Get weather for those coordinates
    weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    weather_data = requests.get(weather_url).json()
    current = weather_data['current_weather']
    
    return {
        "location": full_name,
        "weather": current
    }

