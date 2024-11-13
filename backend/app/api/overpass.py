# backend/app/api/overpass.py

import requests
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

def get_poi_data(city: str, amenity: str = "cafe"):
    """Fetch amenities (POIs) based on city and amenity type from OpenStreetMap Overpass API."""
    try:
        overpass_query = f"""
        [out:json];
        area["name"="{city}"]["admin_level"="8"]->.searchArea;
        node["amenity"="{amenity}"](area.searchArea);
        out;
        """
        
        response = requests.get(OVERPASS_API_URL, params={'data': overpass_query})
        
        if response.status_code != 200:
            logger.error(f"Overpass API Error: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch POI data")

        pois = response.json().get("elements", [])
        return [{"name": poi.get("tags", {}).get("name", "Unknown"), "lat": poi["lat"], "lon": poi["lon"]} for poi in pois]
    
    except Exception as e:
        logger.error(f"Error fetching POIs: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error fetching POIs")
