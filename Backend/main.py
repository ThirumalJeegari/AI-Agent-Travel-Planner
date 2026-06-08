import os
import requests

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")



app = FastAPI()



llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY
)



class TravelRequest(BaseModel):
    place: str
    days: int
    people: int
    budget: float



@tool
def get_weather(place: str):

    url = (f"https://api.openweathermap.org/data/2.5/weather"f"?q={place}"f"&appid={OPENWEATHER_API_KEY}"f"&units=metric")

    response = requests.get(url)
    if response.status_code != 200:
        return "Weather unavailable"

    data = response.json()

    return (
        f"Temperature: {data['main']['temp']} °C, "
        f"Condition: {data['weather'][0]['description']}"
    )



@tool
def web_search(query: str):

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }

    response = requests.post(url,headers=headers,json=payload)

    if response.status_code != 200:
        return "Search failed"

    data = response.json()

    results = []

    for item in data.get("organic", [])[:5]:

        title = item.get("title", "")
        snippet = item.get("snippet", "")

        results.append(
            f"{title}\n{snippet}"
        )

    return "\n\n".join(results)



@tool
def budget_breakdown(budget: float):
    hotel = budget * 0.40
    food = budget * 0.25
    transport = budget * 0.20
    activities = budget * 0.15

    return {f"""
        Hotel: ₹{hotel:.2f}
        Food: ₹{food:.2f}
        Transport: ₹{transport:.2f}
        Activities: ₹{activities:.2f}
    """
    }



tools = [get_weather,web_search,budget_breakdown]



prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
                        """
            You are an AI Travel Planner.

            Use available tools whenever needed.

            Always provide:

            1. Weather
            2. Top Attractions
            3. Day Wise Itinerary
            4. Budget Breakdown
            5. Travel Tips
            """
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)



agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


@app.get("/")
def home():
    return {
        "message": "AI Agent Travel Planner Backend is Running"
    }


@app.post("/plan-trip")
def plan_trip(request: TravelRequest):
    try:
        user_query = f"""
            Plan a trip to {request.place}

            Days: {request.days}
            People: {request.people}
            Budget: ₹{request.budget}

            Get weather.
            Search attractions.
            Calculate budget breakdown.
            Create a complete itinerary.
        """
        result = agent_executor.invoke(
            {
                "input": user_query
            }
        )

        return {
            "response": result["output"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }