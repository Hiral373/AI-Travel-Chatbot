from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

with open('destinations.json', 'r', encoding='utf-8') as f:
    destinations = json.load(f)

with open('itineraries.json', 'r', encoding='utf-8') as f:
    itineraries = json.load(f)

session_data = {
    "destination": None,
    "travel_date": None
}

def get_weather(destination):
    API_KEY = "1aef80f017ed462bbfd61e21d76abd91"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={destination}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return None
        weather = f"{data['main']['temp']}°C, {data['weather'][0]['description'].capitalize()}"
        return weather
    except:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    data = request.get_json()
    user_message = data.get("message", "").lower().strip()
    response = ""

    if any(greet in user_message for greet in ['hello', 'hi', 'hey', 'hii']):
        response = "👋 Hello! How can I assist you in planning your trip?"
    
    elif any(phrase in user_message for phrase in ["i want to go", "travel to", "visit", "to travel"]):
        for dest in destinations:
            if dest["name"].lower() in user_message:
                session_data["destination"] = dest["name"]
                response = f"🌍 You want to go to {dest['name']}. When do you plan to travel?"
                break
        else:
            response = "Please mention a valid city or destination."
    
    elif any(phrase in user_message for phrase in ["after", "in", "today", "tomorrow"]):
        if session_data["destination"]:
            if "today" in user_message:
                travel_date = datetime.today()
            elif "tomorrow" in user_message:
                travel_date = datetime.today() + timedelta(days=1)
            else:
                num_days = [int(s) for s in user_message.split() if s.isdigit()]
                if num_days:
                    travel_date = datetime.today() + timedelta(days=num_days[0])
                else:
                    return jsonify({"reply": "Please provide a valid travel date."})
            
            session_data["travel_date"] = travel_date.strftime("%d-%m-%Y")
            response = f"✅ Your trip to {session_data['destination']} is planned on {session_data['travel_date']}. Do you want to know further information like weather, best time to visit or itinerary?"
        else:
            response = "Please first tell me your destination."
    
    elif user_message in ["yes", "yeah", "yup", "sure"]:
        response = "Great! What would you like to know? Weather, best time to visit, or itinerary?"
    
    elif user_message in ["no", "nope", "not now"]:
        response = "Alright! Do you need any other information from me?"
    
    elif "weather" in user_message:
        if session_data["destination"]:
            weather = get_weather(session_data["destination"])
            if weather:
                response = f"🌤️ Current weather in {session_data['destination']}: {weather}"
            else:
                response = "Sorry, I couldn't fetch the weather information."
        else:
            response = "Please tell me which city you want to know about."
    
    elif "best time" in user_message:
        if session_data["destination"]:
            dest_info = next((d for d in destinations if d["name"] == session_data["destination"]), None)
            if dest_info:
                months = ", ".join(dest_info["best_time_to_visit"])
                response = f"📅 Best time to visit {dest_info['name']} is: {months}."
            else:
                response = "I don't have information about that city."
        else:
            response = "Please mention a city first."
    
    elif "itinerary" in user_message:
        if session_data["destination"]:
            itinerary = itineraries.get(session_data["destination"])
            if itinerary:
                itinerary_details = ""
                if isinstance(itinerary, dict):
                    for day, activities in itinerary.items():
                        itinerary_details += f"\n{day}:\n" + "\n".join(activities) + "\n"
                else:
                    itinerary_details = "\n".join(itinerary)
                response = f"🗺️ Here’s a 3-day itinerary for {session_data['destination']}:{itinerary_details}"
            else:
                response = "Itinerary is not available."
        else:
            response = "Please tell me which city you want an itinerary for."
    
    else:
        response = "🙂 I didn't understand. Please mention a city, region or say 'hello'."
    
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
