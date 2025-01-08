import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from babel.numbers import format_decimal

# Conversion data for quick references
conversion_factors = {
    "Length": {
        "meters to feet": 3.28084,
        "feet to meters": 0.3048,
        "inches to cm": 2.54,
        "cm to inches": 0.393701,
    },
    "Area": {
        "sq meters to hectares": 0.0001,
        "hectares to sq meters": 10000,
        "acres to hectares": 0.404686,
        "hectares to acres": 2.47105,
        "sq feet to acres": 2.2957e-5,
        "acres to sq feet": 43560,
    },
    "Volume": {
        "liters to gallons": 0.264172,
        "gallons to liters": 3.78541,
        "cubic feet to gallons": 7.48052,
        "gallons to cubic feet": 0.133681,
    },
    "Weight": {
        "pounds to kilograms": 0.453592,
        "kilograms to pounds": 2.20462,
        "ounces to grams": 28.3495,
        "grams to ounces": 0.035274,
    },
}

# Initialize session state for saved settings and history
if "saved_settings" not in st.session_state:
    st.session_state["saved_settings"] = {}
if "calculation_history" not in st.session_state:
    st.session_state["calculation_history"] = []

# Function to append to history
def append_history(entry):
    st.session_state["calculation_history"].append(entry)

# Function to format numbers
def format_number(value, locale="en_US"):
    return format_decimal(value, locale=locale)

# Conversion Module
def conversion_module():
    st.header("Conversion Module")
    st.write("Perform quick and precise conversions for farming and agriculture.")

    category = st.selectbox("Select Conversion Category:", list(conversion_factors.keys()))
    options = list(conversion_factors[category].keys())
    conversion = st.selectbox("Select Conversion:", options)
    input_value = st.number_input("Enter Value to Convert:", min_value=0.0, step=0.01)

    if st.button("Convert"):
        factor = conversion_factors[category][conversion]
        result = input_value * factor
        st.success(f"{input_value} converts to {format_number(result)} ({conversion}).")
        append_history({
            "type": "Conversion",
            "category": category,
            "conversion": conversion,
            "input_value": input_value,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# Chemical Dosage Calculator
def chemical_calculator():
    st.header("Chemical Dosage Calculator")
    st.write("Calculate the required chemical dosage for a specific area.")

    total_area = st.number_input("Enter total area recommended (e.g., 10 ha):", min_value=0.0, step=0.1)
    total_chemical = st.number_input("Enter total chemical recommended (e.g., 1 L):", min_value=0.0, step=0.01)
    desired_area = st.number_input("Enter your desired area (e.g., 3 ha):", min_value=0.0, step=0.1)

    if st.button("Calculate Dosage"):
        if total_area > 0 and total_chemical > 0:
            dosage_per_ha = total_chemical / total_area
            required_chemical = dosage_per_ha * desired_area
            st.success(f"You need {format_number(required_chemical)} L of chemical for {format_number(desired_area)} ha.")
            append_history({
                "type": "Chemical Dosage",
                "total_area": total_area,
                "total_chemical": total_chemical,
                "desired_area": desired_area,
                "required_chemical": required_chemical,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            st.error("Please enter valid inputs.")

# Dashboard for History
def dashboard():
    st.header("Dashboard")
    st.write("View your calculation history.")

    # Display History
    st.subheader("Calculation History")
    if st.session_state["calculation_history"]:
        history_df = pd.DataFrame(st.session_state["calculation_history"])
        st.dataframe(history_df)
    else:
        st.info("No history available.")

# Main App
def main():
    st.title("Enhanced Farm Helper: Agriculture Conversion and Tools")
    st.sidebar.title("Navigation")
    options = [
        "Conversion Module",
        "Chemical Calculator",
        "Dashboard",
    ]
    choice = st.sidebar.radio("Choose a tool:", options)

    if choice == "Conversion Module":
        conversion_module()
    elif choice == "Chemical Calculator":
        chemical_calculator()
    elif choice == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()

