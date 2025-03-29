# AI Travel Chatbot

## Overview

The AI Travel Chatbot is a smart assistant that helps users plan their trips by providing destination recommendations, itineraries, weather details, and best travel times. It is built using Flask for the backend and a simple frontend with HTML, CSS, and JavaScript.

## Features

- 🌍 Destination recommendations based on user preferences
- 📅 Travel date planning and confirmation
- ⛅ Real-time weather updates for selected destinations
- 📝 Itinerary suggestions for various locations
- 🎭 Best time to visit recommendations

## Project Structure

```
TRAVEL1/
│-- templates/
│   │-- index.html              # Frontend interface
│-- destinations.json           # Destination details
│-- itineraries.json            # Itinerary plans for cities
│-- main.py                     # Flask backend
│-- preferences.json            # User preferences for budget, travel types, etc.
│-- requirements.txt            # Dependencies
```

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/travel-chatbot.git
   cd travel-chatbot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:

   ```bash
   python main.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.

## Usage

1. Start the chatbot and enter your travel query.
2. Select a destination or request recommendations.
3. Confirm your travel dates.
4. Get additional information like weather, best time to visit, or itinerary.

## Future Improvements

- ✅ Improve chatbot conversation flow
- ✅ Add LangGraph library
- ✅ Integrate Hugging Face to generate responses when the JSON file lacks content

## License

This project is open-source and available under the MIT License.

