import json
import ssl
import urllib.request
import urllib.parse
import tkinter as tk
from tkinter import messagebox

def get_weather():
    city = entry_city.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    context = ssl._create_unverified_context()

    try:
        # Step 1: Geocoding API to find Lat/Lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=en&format=json"
        req_geo = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req_geo, context=context, timeout=10) as response:
            geo_data = json.loads(response.read().decode())

        if "results" not in geo_data or not geo_data["results"]:
            messagebox.showerror("Not Found", f"City '{city}' not found. Please check spelling.")
            return

        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Step 2: Fetch Live Weather & Extra Metrics
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m,surface_pressure"
        req_weather = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req_weather, context=context, timeout=10) as response:
            weather_data = json.loads(response.read().decode())

        current = weather_data["current_weather"]
        temp = current["temperature"]
        wind_speed = current["windspeed"]
        weather_code = current["weathercode"]

        # Extra metrics
        humidity = weather_data.get("hourly", {}).get("relativehumidity_2m", [50])[0]
        pressure = weather_data.get("hourly", {}).get("surface_pressure", [1013])[0]

        # Weather Mapping with Icons & Recommendations
        code_info = {
            0: ("☀️ Clear Sky", "Perfect day for outdoor activities! Don't forget sunscreen."),
            1: ("🌤️ Mainly Clear", "Great weather ahead. Enjoy your day!"),
            2: ("⛅ Partly Cloudy", "Pleasant weather with light clouds."),
            3: ("☁️ Overcast", "Cloudy skies. Keep a light jacket handy."),
            45: ("🌫️ Foggy", "Low visibility! Drive carefully."),
            51: ("🌦️ Light Drizzle", "Slight drizzle. Carrying a small umbrella is recommended."),
            61: ("🌧️ Rain", "It's raining! Carry an umbrella or raincoat."),
            65: ("🌧️ Heavy Rain", "Heavy rainfall expected! Stay indoors if possible."),
            80: ("🌦️ Rain Showers", "Passing rain showers expected."),
            95: ("🌩️ Thunderstorm", "Thunderstorm warning! Avoid open areas.")
        }

        icon_cond, tip = code_info.get(weather_code, ("🌧️ Rainy/Cloudy", "Stay prepared for changing weather conditions."))

        # Update Display
        lbl_location.config(text=f"📍 {city_name}, {country}")
        lbl_temp.config(text=f"{temp:.1f}°C")
        lbl_condition.config(text=icon_cond)
        lbl_wind.config(text=f"💨 Wind: {wind_speed} km/h")
        lbl_humidity.config(text=f"💧 Humidity: {humidity}%")
        lbl_pressure.config(text=f"⏲️ Pressure: {pressure:.0f} hPa")
        lbl_tip.config(text=f"💡 Tip: {tip}")

    except Exception:
        messagebox.showerror("Network Error", "Unable to connect. Check your internet connection.")

def reset_fields():
    entry_city.delete(0, tk.END)
    lbl_location.config(text="📍 --, --")
    lbl_temp.config(text="--°C")
    lbl_condition.config(text="--")
    lbl_wind.config(text="💨 Wind: -- km/h")
    lbl_humidity.config(text="💧 Humidity: --%")
    lbl_pressure.config(text="⏲️ Pressure: -- hPa")
    lbl_tip.config(text="")

# UI Setup
root = tk.Tk()
root.title("OIBSIP - Interactive Weather App")
root.geometry("420x480")
root.configure(bg="#f4f6f7")
root.resizable(False, False)

# Header
tk.Label(root, text="Real-Time Weather Dashboard", bg="#f4f6f7", fg="#2c3e50", font=("Arial", 12, "bold")).pack(pady=(15, 5))

# Input Frame
frame_input = tk.Frame(root, bg="#f4f6f7")
frame_input.pack(pady=5)

entry_city = tk.Entry(frame_input, font=("Arial", 11), width=18, justify="center")
entry_city.pack(side="left", padx=5)

btn_search = tk.Button(frame_input, text="Search", command=get_weather, bg="#2980b9", fg="white", font=("Arial", 9, "bold"), padx=8, pady=2, bd=0, cursor="hand2")
btn_search.pack(side="left", padx=2)

btn_reset = tk.Button(frame_input, text="Reset", command=reset_fields, bg="#7f8c8d", fg="white", font=("Arial", 9, "bold"), padx=8, pady=2, bd=0, cursor="hand2")
btn_reset.pack(side="left", padx=2)

# Card Display Frame
card = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
card.pack(pady=15, padx=20, fill="both", expand=True)

lbl_location = tk.Label(card, text="📍 --, --", font=("Arial", 11, "bold"), bg="#ffffff", fg="#7f8c8d")
lbl_location.pack(pady=(12, 0))

lbl_temp = tk.Label(card, text="--°C", font=("Arial", 36, "bold"), bg="#ffffff", fg="#2c3e50")
lbl_temp.pack(pady=(5, 0))

lbl_condition = tk.Label(card, text="--", font=("Arial", 13, "bold"), bg="#ffffff", fg="#34495e")
lbl_condition.pack(pady=5)

# Metrics Grid
frame_metrics = tk.Frame(card, bg="#ffffff")
frame_metrics.pack(pady=10)

lbl_humidity = tk.Label(frame_metrics, text="💧 Humidity: --%", font=("Arial", 9, "bold"), bg="#ffffff", fg="#555")
lbl_humidity.grid(row=0, column=0, padx=10, pady=2)

lbl_wind = tk.Label(frame_metrics, text="💨 Wind: -- km/h", font=("Arial", 9, "bold"), bg="#ffffff", fg="#555")
lbl_wind.grid(row=0, column=1, padx=10, pady=2)

lbl_pressure = tk.Label(card, text="⏲️ Pressure: -- hPa", font=("Arial", 9), bg="#ffffff", fg="#7f8c8d")
lbl_pressure.pack(pady=2)

# Smart Tip
lbl_tip = tk.Label(card, text="", font=("Arial", 9, "italic"), bg="#ffffff", fg="#27ae60", wraplength=340)
lbl_tip.pack(pady=(10, 12))

root.mainloop()