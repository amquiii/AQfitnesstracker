import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Fitness Tracker", layout="wide")


# Sidebar BMI Calculator 
st.sidebar.header("BMI Calculator")
height_cm = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, value=170)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
bmi = weight_kg / ((height_cm / 100) ** 2)
if bmi < 18.5:
    bmi_category = "Underweight"
elif 18.5 <= bmi < 25:
    bmi_category = "Normal weight"
elif 25 <= bmi < 30:
    bmi_category = "Overweight"
else:
    bmi_category = "Obese"
st.sidebar.metric("BMI", f"{bmi:.1f}", bmi_category)

st.subheader("About Page")
"""The Fitness Tracker application enables users to monitor and manage their daily health and fitness activities, including steps taken, workouts, sleep patterns, calorie consumption, and water intake.

**Outputs Shown:**  
- Daily summaries of activity and health metrics
- Weekly charts illustrating trends in steps, calories, and workout distribution
- Key metrics to monitor and evaluate progress over time"""

#  Initialize Session State 
if "fitness_data" not in st.session_state:
    st.session_state.fitness_data = pd.DataFrame(columns=[
        "Date", "Steps", "Calories", "Sleep", "Water", "Mood"
    ])

# Dashboard Inputs 
st.title(" Fitness Tracker Dashboard")
name = st.text_input("Name")
age = st.number_input("Age", min_value=10, max_value=100)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

st.write("---")

st.subheader("Daily Fitness Entry")
today = st.date_input("Date", value=date.today())
steps = st.number_input("Steps Taken", min_value=0)
calories = st.number_input("Calories Burned", min_value=0)
sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0)
water_intake = st.number_input("Water Intake (liters)", 0.0, 10.0, 2.0, step=0.1)
mood = st.radio("Mood Today", ["Happy", "Neutral", "Tired", "Sad"])



# Submit Entry 
if st.button("Submit Entry"):
    # Save entry to session state
    new_entry = pd.DataFrame({
        "Date": [today],
        "Steps": [steps],
        "Calories": [calories],
        "Sleep": [sleep_hours],
        "Water": [water_intake],
        "Mood": [mood]
    })
     # Ensure the Date column is only the day (no time)
    new_entry["Date"] = pd.to_datetime(new_entry["Date"]).dt.date

    st.session_state.fitness_data = pd.concat(
        [st.session_state.fitness_data, new_entry],
        ignore_index=True
    )

    st.success("Fitness data submitted!")
    

    
    
    #  Show Charts from User Data 
    st.subheader("📊 Weekly Progress (User Submitted Data)")
    df = st.session_state.fitness_data

    if not df.empty:
        # Steps chart
        st.subheader("Steps  Chart")
        st.bar_chart(df.set_index("Date")["Steps"])

        # Calories chart
        st.subheader("Calories Chart")
        st.line_chart(df.set_index("Date")["Calories"])

        # Sleep chart
        st.subheader("Sleep Chart")
        st.line_chart(df.set_index("Date")["Sleep"])

        # Water intake chart
        st.subheader("Water Intake Chart")
        st.bar_chart(df.set_index("Date")["Water"])

        # Mood distribution
        st.subheader("Daily Mood")
        st.subheader("Mood Distribution")
        mood_counts = df["Mood"].value_counts()
        st.bar_chart(mood_counts)