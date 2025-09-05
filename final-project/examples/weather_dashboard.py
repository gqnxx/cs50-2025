# Example 3: Weather Dashboard (API Integration)

"""
Weather Dashboard - A web application that displays weather information.

Features:
- Current weather for any city
- 5-day weather forecast
- Weather history
- Favorite cities
- Responsive design

Tech Stack:
- Backend: Python Flask
- API: OpenWeatherMap API
- Frontend: HTML, CSS, JavaScript
- Database: SQLite for favorites
"""

import requests
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'weather-app-secret-key'

# OpenWeatherMap API configuration
# Sign up at https://openweathermap.org/api to get your free API key
API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your-api-key-here')
BASE_URL = 'http://api.openweathermap.org/data/2.5/'

def init_db():
    """Initialize database for storing favorite cities."""
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE NOT NULL,
            country_code TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL,
            temperature REAL,
            description TEXT,
            humidity INTEGER,
            wind_speed REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_weather_data(city_name):
    """Fetch current weather data from OpenWeatherMap API."""
    try:
        url = f"{BASE_URL}weather"
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
            'feels_like': round(data['main']['feels_like']),
            'pressure': data['main']['pressure'],
            'visibility': data.get('visibility', 0) // 1000  # Convert to km
        }
        
        # Save to history
        save_weather_history(weather_info)
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
    except KeyError as e:
        print(f"Data parsing error: {e}")
        return None

def get_forecast_data(city_name):
    """Fetch 5-day weather forecast."""
    try:
        url = f"{BASE_URL}forecast"
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Process forecast data (every 3 hours, take daily high/low)
        daily_forecast = {}
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            temp = item['main']['temp']
            
            if date not in daily_forecast:
                daily_forecast[date] = {
                    'date': date,
                    'high': temp,
                    'low': temp,
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon']
                }
            else:
                daily_forecast[date]['high'] = max(daily_forecast[date]['high'], temp)
                daily_forecast[date]['low'] = min(daily_forecast[date]['low'], temp)
        
        # Convert to list and round temperatures
        forecast_list = []
        for forecast in list(daily_forecast.values())[:5]:  # Next 5 days
            forecast['high'] = round(forecast['high'])
            forecast['low'] = round(forecast['low'])
            forecast_list.append(forecast)
        
        return forecast_list
        
    except requests.exceptions.RequestException as e:
        print(f"Forecast API Error: {e}")
        return []

def save_weather_history(weather_info):
    """Save weather data to history."""
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO weather_history 
        (city_name, temperature, description, humidity, wind_speed)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        weather_info['city'],
        weather_info['temperature'],
        weather_info['description'],
        weather_info['humidity'],
        weather_info['wind_speed']
    ))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Home page."""
    return render_template('weather_index.html')

@app.route('/weather/<city_name>')
def weather(city_name):
    """Display weather for a specific city."""
    weather_data = get_weather_data(city_name)
    forecast_data = get_forecast_data(city_name)
    
    if weather_data:
        return render_template('weather_display.html', 
                             weather=weather_data, 
                             forecast=forecast_data)
    else:
        return render_template('weather_error.html', 
                             error="City not found or API error")

@app.route('/search', methods=['POST'])
def search():
    """Handle weather search."""
    city_name = request.form.get('city')
    if city_name:
        return redirect(url_for('weather', city_name=city_name))
    return redirect(url_for('index'))

@app.route('/api/weather/<city_name>')
def api_weather(city_name):
    """API endpoint for weather data."""
    weather_data = get_weather_data(city_name)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'City not found'}), 404

@app.route('/favorites')
def favorites():
    """Display favorite cities."""
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('SELECT city_name, country_code FROM favorites ORDER BY city_name')
    favorites_list = cursor.fetchall()
    conn.close()
    
    # Get current weather for each favorite
    favorites_weather = []
    for city, country in favorites_list:
        weather_data = get_weather_data(city)
        if weather_data:
            favorites_weather.append(weather_data)
    
    return render_template('favorites.html', favorites=favorites_weather)

@app.route('/add_favorite/<city_name>')
def add_favorite(city_name):
    """Add city to favorites."""
    # First verify city exists
    weather_data = get_weather_data(city_name)
    if weather_data:
        conn = sqlite3.connect('weather.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO favorites (city_name, country_code) VALUES (?, ?)',
                (weather_data['city'], weather_data['country'])
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # City already in favorites
        finally:
            conn.close()
    
    return redirect(url_for('weather', city_name=city_name))

@app.route('/remove_favorite/<city_name>')
def remove_favorite(city_name):
    """Remove city from favorites."""
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM favorites WHERE city_name = ?', (city_name,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('favorites'))

@app.route('/history')
def history():
    """Display weather search history."""
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city_name, temperature, description, timestamp
        FROM weather_history
        ORDER BY timestamp DESC
        LIMIT 50
    ''')
    history_data = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', history=history_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# Usage:
# 1. Sign up for free API key at https://openweathermap.org/api
# 2. Set environment variable: export OPENWEATHER_API_KEY=your_api_key
# 3. pip install flask requests
# 4. python weather_dashboard.py
# 5. Visit http://localhost:5000

# HTML Templates needed:
# - templates/weather_index.html (search form)
# - templates/weather_display.html (weather display)
# - templates/weather_error.html (error page)
# - templates/favorites.html (favorites page)
# - templates/history.html (history page)
