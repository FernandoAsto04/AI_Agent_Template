import requests

"""Obtiene la temperatura actual y condiciones del clima para una ciudad o distrito."""

def get_current_weather(location_name: str) -> dict:
    
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_name}&count=1&language=es&format=json"
        geo_res = requests.get(geo_url).json()

        if not geo_res.get("results"):
            return {"error": f"No se encontró la ubicación: {location_name}"}

        place = geo_res["results"][0]
        lat, lon = place["latitude"], place["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m&timezone=auto"
        weather_res = requests.get(weather_url).json()
        current = weather_res.get("current", {})

        return {
            "ubicacion": place.get("name"),
            "temperatura": f"{current.get('temperature_2m')} °C",
            "humedad": f"{current.get('relative_humidity_2m')} %"
        }
    except Exception as e:
        return {"error": f"Error consultando el clima: {str(e)}"}