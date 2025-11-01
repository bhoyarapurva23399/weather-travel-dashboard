import requests
from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

API_KEY = "your_openweathermap_api_key_here"  # You can leave it like this for now
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city.title(),
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed']
                }
            else:
                weather_data = {'error': 'City not found! Please try again.'}

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Travel Dashboard</title>
        <style>
            body { font-family: Arial; background: #f0f4f8; text-align: center; padding: 50px; }
            form { margin: 20px auto; }
            input { padding: 10px; border-radius: 8px; border: 1px solid #ccc; }
            button { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; }
            .card { background: white; padding: 20px; margin: 20px auto; width: 300px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>🌤 Weather Travel Dashboard</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter City Name" required>
            <button type="submit">Get Weather</button>
        </form>

        {% if weather_data %}
            {% if weather_data.error %}
                <p style="color:red;">{{ weather_data.error }}</p>
            {% else %}
                <div class="card">
                    <h2>{{ weather_data.city }}</h2>
                    <p>🌡 Temperature: {{ weather_data.temperature }}°C</p>
                    <p>💨 Wind Speed: {{ weather_data.wind }} m/s</p>
                    <p>💧 Humidity: {{ weather_data.humidity }}%</p>
                    <p>🌈 Condition: {{ weather_data.description }}</p>
                </div>
            {% endif %}
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
