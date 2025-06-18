# Weather Application

A Streamlit-based web application that displays weather information and location for any city using the Open-Meteo API and OpenStreetMap.

## Features

- City-based weather lookup
- Current weather conditions display
- 24-hour weather forecast
- Interactive map showing the city location
- No API key required

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run weather_app.py
```

The application will open in your default web browser. Enter a city name in the text input field to see the weather information and location map.

## Testing

Run the unit tests:
```bash
python -m unittest test_weather_app.py
```

## Technologies Used

- Streamlit: Web application framework
- Open-Meteo: Weather data API
- OpenStreetMap (via Folium): Map visualization
- GeoPy: Geocoding service