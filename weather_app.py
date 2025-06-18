import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from datetime import datetime

def get_coordinates(city_name):
    """Get latitude and longitude for a given city name."""
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude, True
        return None, None, False
    except Exception as e:
        st.error(f"Error getting coordinates: {str(e)}")
        return None, None, False

def get_weather_data(lat, lon):
    """Fetch weather data from Open-Meteo API."""
    try:
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "temperature_2m,precipitation_probability,weathercode",
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json(), True
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None, False

def get_weather_description(weathercode):
    """Convert weather code to human-readable description."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return weather_codes.get(weathercode, "Unknown")

def create_map(lat, lon, city_name):
    """Create a folium map centered on the given coordinates."""
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker(
        [lat, lon],
        popup=city_name,
        tooltip=city_name
    ).add_to(m)
    return m

def main():
    st.title("Weather App 🌤️")
    
    # City input
    city = st.text_input("Enter city name:", "")
    
    if city:
        # Get coordinates for the city
        lat, lon, success = get_coordinates(city)
        
        if success:
            # Fetch weather data
            weather_data, success = get_weather_data(lat, lon)
            
            if success:
                # Display current weather
                current = weather_data["current_weather"]
                
                st.subheader(f"Current Weather in {city}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Temperature", f"{current['temperature']}°C")
                    st.metric("Wind Speed", f"{current['windspeed']} km/h")
                
                with col2:
                    weather_desc = get_weather_description(current['weathercode'])
                    st.metric("Weather", weather_desc)
                    st.metric("Wind Direction", f"{current['winddirection']}°")
                
                # Display map
                st.subheader("Location Map")
                m = create_map(lat, lon, city)
                folium_static(m)
                
                # Display hourly forecast
                st.subheader("Hourly Forecast")
                hourly_data = weather_data["hourly"]
                hours = hourly_data["time"][:24]  # Next 24 hours
                temps = hourly_data["temperature_2m"][:24]
                precip_prob = hourly_data["precipitation_probability"][:24]
                
                # Create a DataFrame for the hourly forecast
                import pandas as pd
                hourly_df = pd.DataFrame({
                    "Time": [datetime.fromisoformat(h).strftime("%H:00") for h in hours],
                    "Temperature (°C)": temps,
                    "Precipitation Probability (%)": precip_prob
                })
                
                st.dataframe(hourly_df)
        
        else:
            st.error("Could not find the specified city. Please check the spelling and try again.")

if __name__ == "__main__":
    main()