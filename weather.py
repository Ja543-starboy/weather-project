# 🌦️ Weather Application - Single File Version
import requests
import json
from datetime import datetime
from getpass import getpass

class WeatherApp:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.units = "metric"  # Change to "imperial" for Fahrenheit
        self.load_api_key()
        
    def load_api_key(self):
        """Load or prompt for API key"""
        try:
            with open("weather_api_key.txt", "r") as f:
                self.api_key = f.read().strip()
        except FileNotFoundError:
            print("API key not found. Get one from https://openweathermap.org/api")
            self.api_key = getpass("Enter your OpenWeatherMap API key: ")
            with open("weather_api_key.txt", "w") as f:
                f.write(self.api_key)
            print("API key saved for future use.")

    def get_weather(self, location):
        """Fetch weather data from API"""
        if not self.api_key:
            print("API key not configured.")
            return None
            
        try:
            params = {
                'q': location,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def display_weather(self, weather_data):
        """Display formatted weather information"""
        if not weather_data:
            print("No weather data available.")
            return

        try:
            main = weather_data['main']
            weather = weather_data['weather'][0]
            sys = weather_data['sys']
            wind = weather_data['wind']
            
            print("\n=== Current Weather ===")
            print(f"📍 Location: {weather_data['name']}, {sys['country']}")
            print(f"🌤️ Conditions: {weather['description'].capitalize()}")
            print(f"🌡️ Temperature: {main['temp']}°C (Feels like {main['feels_like']}°C)")
            print(f"💧 Humidity: {main['humidity']}%")
            print(f"💨 Wind: {wind['speed']} m/s, Direction: {wind.get('deg', 'N/A')}°")
            print(f"⏲️ Pressure: {main['pressure']} hPa")
            
            sunrise = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M')
            print(f"🌅 Sunrise: {sunrise} | 🌇 Sunset: {sunset}")
            
        except KeyError as e:
            print(f"Error parsing weather data: Missing key {e}")

    def run(self):
        """Main application loop"""
        print("\n" + "="*40)
        print("🌦️ Welcome to the Weather Application 🌦️")
        print("="*40)
        print("Enter 'quit' to exit\n")
        
        while True:
            location = input("Enter city name or zip code,country (e.g., London,UK): ").strip()
            
            if location.lower() in ('quit', 'exit'):
                print("\nGoodbye! Have a nice day! ☀️")
                break
                
            if not location:
                print("⚠️ Please enter a location.")
                continue
                
            weather_data = self.get_weather(location)
            self.display_weather(weather_data)

if __name__ == "__main__":
    app = WeatherApp()
    app.run()