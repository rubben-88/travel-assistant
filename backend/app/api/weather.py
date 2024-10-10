import requests
from app.config import OPENWEATHERMAP_API_KEY

# Base URLs
ONE_CALL_API_URL = "https://api.openweathermap.org/data/3.0/onecall"
GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"

def get_lat_lon(city_name):
    """Fetch latitude and longitude for a city using OpenWeather Geocoding API."""
    params = {
        "q": city_name,
        "limit": 1,  # We only need the first result
        "appid": OPENWEATHERMAP_API_KEY
    }
    response = requests.get(GEOCODING_API_URL, params=params)
    if response.status_code == 200 and response.json():
        location = response.json()[0]
        return location["lat"], location["lon"]
    return None, None

def query_weather(city, date):
    """Query weather using the One Call API based on city name."""
    
    # Get latitude and longitude of the city
    lat, lon = get_lat_lon(city)
    
    if lat is None or lon is None:
        return "Weather data not available: Could not fetch coordinates for the city"
    
    print(f"Querying weather for: city={city}, lat={lat}, lon={lon}, date={date}")
    
    # Call One Call API with latitude and longitude
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",  # You can change this to 'imperial' if needed
        "exclude": "minutely,hourly"  # Optional: exclude unnecessary data
    }
    
    response = requests.get(ONE_CALL_API_URL, params=params)
    
    if response.status_code == 200:
        weather = response.json()
        
        # Extract current weather data
        current_weather = weather.get('current', {})
        description = current_weather.get('weather', [{}])[0].get('description', 'No description')
        temperature = current_weather.get('temp', 'N/A')
        
        # Here, date is ignored because One Call API gives current data. 
        # You can store or compare dates manually if needed.
        
        return f"Current weather in {city}: {description}, Temp: {temperature}°C"
    
    return "Weather data not available"
