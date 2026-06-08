# ✈️ AI Travel Planner Agent

An AI-powered Travel Planner that uses a **Single AI Agent with Multiple Tools** to generate personalized travel itineraries.

The application integrates:

* 🌤 Live Weather Data (OpenWeather API)
* 🔍 Real-Time Web Search (Serper API)
* 💰 Budget Analysis Tool
* 🤖 Groq LLM (Llama 3.3 70B)
* ⚡ FastAPI Backend
* 🎨 Streamlit Frontend

---

# 🚀 Features

### AI Agent

The AI Agent acts as the central decision-maker and combines information from multiple tools to create a complete travel plan.

### Weather Tool

Fetches real-time weather information for the selected destination using OpenWeather API.

Example:

* Temperature
* Weather Condition
* Climate Information

### Web Search Tool

Searches the internet for:

* Tourist Attractions
* Popular Places
* Travel Recommendations
* Destination Highlights

using Serper Search API.

### Budget Tool

Calculates travel budgets based on:

* Number of Days
* Number of People
* Total Budget

Provides:

* Hotel Budget
* Food Budget
* Transportation Budget
* Activities Budget

### AI Travel Plan Generator

Generates:

* Trip Overview
* Weather Summary
* Tourist Attractions
* Day-wise Itinerary
* Budget Breakdown
* Travel Tips

---

# 🏗 Project Architecture

User

↓

Streamlit Frontend

↓

FastAPI Backend

↓

AI Agent

├── Weather Tool (OpenWeather API)

├── Web Search Tool (Serper API)

└── Budget Tool

↓

Groq LLM

↓

Travel Plan Response

---

# 📂 Project Structure

```text
AI_Agent_Travel_Planner/
│
├── Backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── Frontend/
│   ├── app.py
│   └── requirements.txt
│
├── README.md
└── .gitignore
```

---

# 🛠 Technologies Used

## Backend

* FastAPI
* Python
* Requests
* LangChain Groq

## Frontend

* Streamlit

## APIs

* OpenWeather API
* Serper Search API
* Groq API

---

# 🔑 Environment Variables

Create a `.env` file inside the Backend folder.

```env
GROQ_API_KEY=your_groq_api_key

OPENWEATHER_API_KEY=your_openweather_api_key

SERPER_API_KEY=your_serper_api_key
```

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/AI_Agent_Travel_Planner.git

cd AI_Agent_Travel_Planner
```

---

# Backend Setup

Navigate to Backend:

```bash
cd Backend
```

Create Virtual Environment:

```bash
python -m venv .venv
```

Activate Environment:

Windows

```bash
.venv\Scripts\activate
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Run Backend:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

Navigate to Frontend:

```bash
cd Frontend
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Run Frontend:

```bash
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# API Endpoint

## Health Check

```http
GET /
```

Response:

```json
{
  "message": "AI Travel Planner Running"
}
```

---

## Generate Travel Plan

```http
POST /plan-trip
```

Request Body:

```json
{
  "query": "Plan a Goa trip",
  "place": "Goa",
  "days": 3,
  "people": 4,
  "budget": 100000
}
```

Response:

```json
{
  "response": "Generated Travel Plan...",
  "weather": {
    "temperature": 29,
    "condition": "clear sky"
  },
  "budget": 100000
}
```

---

# ☁️ Deployment on Render

## Deploy Backend

1. Push code to GitHub.
2. Login to Render.
3. Create New Web Service.
4. Connect GitHub Repository.

Settings:

Root Directory:

```text
Backend
```

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Add Environment Variables:

```env
GROQ_API_KEY=xxxx

OPENWEATHER_API_KEY=xxxx

SERPER_API_KEY=xxxx
```

Deploy.

---

# Sample Use Case

Input:

* Place: Goa
* Days: 4
* People: 5
* Budget: ₹100000

Output:

* Weather Information
* Top Attractions
* Day-wise Travel Plan
* Budget Distribution
* Travel Tips

---

# Learning Outcomes

This project demonstrates:

* AI Agent Development
* API Integration
* FastAPI Backend Development
* Streamlit Frontend Development
* Prompt Engineering
* LLM Integration
* Multi-Tool Agent Architecture
* Real-Time Data Processing

---

# Future Enhancements

* Hotel Recommendation System
* Flight Price Integration
* Google Maps Integration
* PDF Travel Report Generation
* Multi-City Travel Planning
* Travel Expense Tracking

---

# Author
Thirumal Jeegari


