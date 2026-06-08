import streamlit as st
import requests

BACKEND_URL = "https://ai-agent-travel-planner.onrender.com"

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️"
)

st.title("✈️ AI Travel Planner")

place = st.text_input("Place", value="Goa")

days = st.number_input(
    "Days",
    min_value=1,
    value=3
)

people = st.number_input(
    "Number of People",
    min_value=1,
    value=2
)

budget = st.number_input(
    "Budget (₹)",
    min_value=1000.0,
    value=50000.0,
    step=1000.0
)

if st.button("Generate Travel Plan"):

    payload = {
        "place": place,
        "days": int(days),
        "people": int(people),
        "budget": float(budget)
    }

    try:

        with st.spinner("Generating Travel Plan..."):

            response = requests.post(
                f"{BACKEND_URL}/plan-trip",
                json=payload,
                timeout=120
            )

        if response.status_code != 200:
            st.error(response.text)

        else:

            result = response.json()

            if "response" in result:

                st.subheader("🌤 Weather")

                weather = result["weather"]
                st.write(f"Temperature: {weather['temperature']} °C")
                st.write(f"Condition: {weather['condition']}")

                st.subheader("💰 Budget Breakdown")

                budget = result["budget_breakdown"]
                st.write(f"🏨 Hotel: ₹{budget['hotel']}")
                st.write(f"🍽 Food: ₹{budget['food']}")
                st.write(f"🚕 Transport: ₹{budget['transport']}")
                st.write(f"🎯 Activities: ₹{budget['activities']}")

            else:
                st.error(result.get("error", "Unknown Error"))

    except Exception as e:
        st.error(f"Connection Error: {str(e)}")