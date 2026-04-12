from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import os
import requests
load_dotenv()


# @tool(name="get_weather", description="Get the weather data for a given city")
# def get_weather(city_name: str) -> str:
#     geo_url = f"https://open-meteo.com{city_name}&count=1&language=en&format=json"
#     geo_resp = requests.get(geo_url).json()
    
#     if not geo_resp.get('results'):
#         return f"City '{city_name}' not found."
    
#     # Extract location details
#     location = geo_resp['results'][0]
#     lat, lon = location['latitude'], location['longitude']
#     full_name = f"{location['name']}, {location.get('country', '')}"
    
#     # 2. Get weather for those coordinates
#     weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
#     weather_data = requests.get(weather_url).json()
#     current = weather_data['current_weather']
    
#     return {
#         "location": full_name,
#         "weather": current    
#     }

@tool
def web_search_tool(query: str) -> str:
    """Search the web for information."""
    # Create the search engine
    tavily = TavilySearch(
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        max_results=3,
        include_raw_content=True # Ensure the agent gets the full text, not just snippets
    )

    # Invoke and return
    results = tavily.invoke(query)
    return results


if __name__ == "__main__":
    # To test a Tool object in LangChain, use .invoke()
    print(web_search_tool.invoke("what is ollama"))