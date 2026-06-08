import os
import requests

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_groq import ChatGroq

# =====================================================
# ENV VARIABLES
# =====================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI()

# =====================================================
# LLM
# =====================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY
)

# =====================================================
# REQUEST MODEL
# =====================================================

class TravelRequest(BaseModel):
    place: str
    days: int
    people: int
    budget: float

# =====================================================
# WEATHER TOOL
# =====================================================

def get_weather(place: str):

    try:

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={place}"
            f"&appid={OPENWEATHER_API_KEY}"
            f"&units=metric"
        )

        response = requests.get(url)

        if response.status_code != 200:
            return "Weather unavailable"

        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"]
        }

    except Exception as e:
        return str(e)

# =====================================================
# SEARCH TOOL
# =====================================================

def web_search(query: str):

    try:

        url = "https://google.serper.dev/search"

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return "Search failed"

        data = response.json()

        results = []

        for item in data.get("organic", [])[:5]:

            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet")
            })

        return results

    except Exception as e:
        return str(e)

# =====================================================
# BUDGET TOOL
# =====================================================

def budget_breakdown(budget: float):

    hotel = budget * 0.40
    food = budget * 0.25
    transport = budget * 0.20
    activities = budget * 0.15

    return {
        "hotel": round(hotel, 2),
        "food": round(food, 2),
        "transport": round(transport, 2),
        "activities": round(activities, 2)
    }

# =====================================================
# ROUTES
# =====================================================

@app.get("/")
def home():
    return {
        "message": "AI Travel Planner Running"
    }

@app.post("/plan-trip")
def plan_trip(request: TravelRequest):

    try:

        weather = get_weather(request.place)

        search_results = web_search(
            f"{request.place} tourist attractions"
        )

        budget_info = budget_breakdown(
            request.budget
        )

        prompt = f"""
You are an expert AI Travel Planner.

Trip Details:
Place: {request.place}
Days: {request.days}
People: {request.people}
Budget: ₹{request.budget}

Weather:
{weather}

Tourist Information:
{search_results}

Budget Breakdown:
{budget_info}

Create:

1. Trip Overview
2. Weather Summary
3. Top Attractions
4. Day-wise Itinerary
5. Budget Breakdown
6. Travel Tips
"""

        response = llm.invoke(prompt)

        return {
            "response": response.content,
            "weather": weather,
            "budget_breakdown": budget_info
        }

    except Exception as e:

        return {
            "error": str(e)
        }