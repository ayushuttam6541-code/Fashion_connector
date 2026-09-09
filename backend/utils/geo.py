import math
from datetime import datetime
from typing import Tuple, List

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def calculate_bounding_box(lat: float, lon: float, radius_km: float) -> Tuple[float, float, float, float]:
    """
    Calculate bounding box coordinates for a given center point and radius
    Returns (min_lat, max_lat, min_lon, max_lon)
    """
    # Approximate conversions
    lat_delta = radius_km / 111.0  # 1 degree latitude ≈ 111 km
    lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
    
    min_lat = lat - lat_delta
    max_lat = lat + lat_delta
    min_lon = lon - lon_delta
    max_lon = lon + lon_delta
    
    return (min_lat, max_lat, min_lon, max_lon)

def format_distance(distance_km: float) -> str:
    """Format distance for display"""
    if distance_km < 1:
        return f"{int(distance_km * 1000)} m away"
    else:
        return f"{distance_km:.1f} km away"

def is_shop_open(timings: dict, current_time = None) -> bool:
    """
    Check if a shop is currently open based on its timings
    timings format: {"Monday": "11:00 AM - 10:00 PM", ...}
    """
    if current_time is None:
        current_time = datetime.now()
    
    day_name = current_time.strftime("%A")
    
    if day_name not in timings:
        return False
    
    timing_str = timings[day_name]
    
    try:
        # Parse timing string (e.g., "11:00 AM - 10:00 PM")
        parts = timing_str.split(" - ")
        if len(parts) != 2:
            return False
        
        open_time_str, close_time_str = parts
        
        # Convert to 24-hour format
        def parse_time(time_str):
            time_str = time_str.strip()
            is_pm = "PM" in time_str
            is_am = "AM" in time_str
            time_str = time_str.replace("AM", "").replace("PM", "").strip()
            
            hours, minutes = map(int, time_str.split(":"))
            
            if is_pm and hours != 12:
                hours += 12
            elif is_am and hours == 12:
                hours = 0
                
            return hours, minutes
        
        open_hour, open_min = parse_time(open_time_str)
        close_hour, close_min = parse_time(close_time_str)
        
        current_hour = current_time.hour
        current_min = current_time.minute
        
        current_minutes = current_hour * 60 + current_min
        open_minutes = open_hour * 60 + open_min
        close_minutes = close_hour * 60 + close_min
        
        return open_minutes <= current_minutes <= close_minutes
        
    except Exception:
        return False