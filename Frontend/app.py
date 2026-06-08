import streamlit as st
import requests



BACKEND_URL = "https://ai-agent-travel-planner.onrender.com"



st.set_page_config(page_title="AI Travel Planner",page_icon="✈️")


st.title("✈️ AI Travel Planner")

st.write("Plan your trip using AI Agent + Weather + Web Search + Budget Tools")


place = st.text_input("Enter the Place")

days = st.number_input("Days",min_value=1,value=3)

people = st.number_input("Number of People",min_value=1,value=2)

budget = st.number_input("Enter Your Budget (₹)",min_value=1000,value=50000,step=1000)

if st.button("Generate Travel Plan"):

    payload = {
        "place": place,
        "days": int(days),
        "people": int(people),
        "budget": float(budget)
    }
    try:

        with st.spinner("Generating AI Travel Plan..."):

            response = requests.post(f"{BACKEND_URL}/plan-trip",json=payload,)

            result = response.json()

        if "response" in result:

            st.subheader("Travel Plan Ready")
            st.markdown(result["response"])

        else:
            st.error(result.get("error","Unknown Error"))

    except Exception as e:
        st.error(f"Connection Error: {str(e)}")

