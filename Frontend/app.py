import streamlit as st
import requests

BACKEND_URL = "https://ai-agent-travel-planner.onrender.com"


st.title("✈️ AI Travel Planner")

st.markdown("Plan your trip using AI, Live Weather, Web Search and Budget Analysis.")

query = st.text_area(
    "Describe your trip",
    placeholder="Example: Plan a family trip to Goa with sightseeing and beach activities."
)

place = st.text_input(
    "Place",
    value="Goa"
)

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
    min_value=1000,
    value=50000,
    step=1000
)

if st.button("Generate Travel Plan"):

    payload = {
        "query": query,
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

            result = response.json()

            if "response" in result:

                st.success("Travel Plan Ready")

                st.subheader("Trip Information")

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"📍 Place: {result['place']}")
                    st.write(f"📅 Days: {result['days']}")

                with col2:
                    st.write(f"👥 People: {result['people']}")
                    st.write(f"💰 Budget: ₹{result['budget']:,.0f}")

                st.divider()

                st.subheader("🌤 Weather")

                weather = result["weather"]

                if isinstance(weather, dict):
                    st.write(
                        f"Temperature: {weather['temperature']}°C"
                    )
                    st.write(
                        f"Condition: {weather['condition']}"
                    )
                else:
                    st.write(weather)

                st.divider()

                st.subheader("🗺 AI Travel Plan")

                st.markdown(result["response"])

            else:

                st.error(
                    result.get("error", "Unknown Error")
                )

    except Exception as e:

        st.error(f"Connection Error: {str(e)}")