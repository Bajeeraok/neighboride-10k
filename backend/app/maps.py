import os
from geopy.geocoders import Nominatim
import requests
from typing import Tuple

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_address(address: str) -> Tuple[float, float]:
    geolocator = Nominatim(user_agent="neighboride")
    location = geolocator.geocode(address + ", Charlotte, NC")
    if location:
        return location.latitude, location.longitude
    return 0.0, 0.0

def get_route_distance(origin: str, destination: str) -> float:
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        return data['rows'][0]['elements'][0]['distance']['value'] / 1609.34 # Meters to miles
    return 0.0