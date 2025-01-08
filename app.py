import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from babel.numbers import format_decimal

# Initialize session state for saved settings and history
if "saved_settings" not in st.session_state:
    st.session_state["saved_settings"] = {}
if "calculation_history" not in st.session_state:
    st.session_state["calculation_history"] = []

# Function to format numbers
def format_number(value, locale="en_US"):
    return format_decimal(value, locale=locale)

# Function to save settings
def save_settings(name, settings):
    st.session_state["saved_settings"][name] = settings
    st.success(f"Settings '{name}' saved successfully!")

# Function to append to history
def append_history(entry):
    st.session_state["calculation_history"].append(entry)

# Chemical Dosage Calculator
def chemical_calculator():
    st.header("Chemical Dosage Calculator")
    st.write("Calculate the required chemical dosage for a specific area.")

    # Input fields
    total_area = st.number_input("Total area recommended (e.g., 10 ha):", min_value=0.0, step=0.1)
    total_chemical = st.number_input("Total chemical recommended (e.g., 1 L):", min_value=0.0, step=0.01)
    desired_area = st.number_input("Your desired area (e.g., 3 ha):", min_value=0.0, step=0.1)

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

# Unit Converter
def unit_converter():
    st.header("Unit Converter")
    st.write("Convert between common units for chemicals, water, and land.")

    # Unit options
    unit_options = ["Liters (L)", "Milliliters (mL)", "Hectares (ha)", "Acres"]
    from_unit = st.selectbox("From Unit:", unit_options)
    to_unit = st.selectbox("To Unit:", unit_options)
    value = st.number_input(f"Enter value in {from_unit}:", min_value=0.0, step=0.01)

    conversion_factors = {
        ("Liters (L)", "Milliliters (mL)"): 1000,
        ("Milliliters (mL)", "Liters (L)"): 0.001,
        ("Hectares (ha)", "Acres"): 2.47105,
        ("Acres", "Hectares (ha)"): 0.404686,
    }

    if st.button("Convert Units"):
        if (from_unit, to_unit) in conversion_factors:
            converted_value = value * conversion_factors[(from_unit, to_unit)]
            st.success(f"{value} {from_unit} is equal to {converted_value} {to_unit}.")
            append_history({
                "type": "Unit Conversion",
                "from_unit": from_unit,
                "to_unit": to_unit,
                "original_value": value,
                "converted_value": converted_value,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        elif from_unit == to_unit:
            st.info("Units are the same. No conversion needed.")
        else:
            st.error("Conversion not available for the selected units.")

# Fertilizer Mixing Ratio
def fertilizer_mixer():
    st.header("Fertilizer Mixing Ratio")
    st.write("Calculate mixing ratios for fertilizers or chemicals.")

    total_volume = st.number_input("Enter total chemical volume (L):", min_value=0.0, step=0.01)
    ratio = st.text_input("Enter ratio (e.g., 10:20:10):")

    if st.button("Calculate Mixing Ratio"):
        try:
            parts = list(map(int, ratio.split(":")))
            total_parts = sum(parts)
            amounts = [round((part / total_parts) * total_volume, 2) for part in parts]
            st.success(f"Mixing amounts: {amounts} L for ratio {ratio}.")
            append_history({
                "type": "Fertilizer Mixing",
                "total_volume": total_volume,
                "ratio": ratio,
                "amounts": amounts,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except ValueError:
            st.error("Invalid ratio format. Use numbers separated by colons (e.g., 10:20:10).")

# Water Requirements
def water_requirements():
    st.header("Water Requirements")
    st.write("Calculate water needed for chemical dilution.")

    chemical_volume = st.number_input("Chemical volume (L):", min_value=0.0, step=0.01)
    dilution_rate = st.number_input("Dilution rate (e.g., 1:100):", min_value=0.0, step=0.1)

    if st.button("Calculate Water Volume"):
        if dilution_rate > 0:
            water_volume = chemical_volume * dilution_rate
            st.success(f"You need {water_volume} L of water to dilute {chemical_volume} L of chemical.")
            append_history({
                "type": "Water Requirement",
                "chemical_volume": chemical_volume,
                "dilution_rate": dilution_rate,
                "water_volume": water_volume,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            st.error("Please enter a valid dilution rate.")

# Dashboard for History
def dashboard():
    st.header("Dashboard")
    st.write("View your saved settings and calculation history.")

    # Saved Settings
    st.subheader("Saved Settings")
    settings_name = st.text_input("Save current settings (name):")
    if st.button("Save Settings"):
        current_settings = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "history": st.session_state["calculation_history"],
        }
        save_settings(settings_name, current_settings)

    # Display History
    st.subheader("Calculation History")
    if st.session_state["calculation_history"]:
        history_df = pd.DataFrame(st.session_state["calculation_history"])
        st.dataframe(history_df)
    else:
        st.info("No history available.")

# Main App
def main():
    st.title("Farm Helper: Chemical and Fertilizer Calculator")
    st.sidebar.title("Navigation")
    options = [
        "Chemical Calculator",
        "Unit Converter",
        "Fertilizer Mixer",
        "Water Requirements",
        "Dashboard",
    ]
    choice = st.sidebar.radio("Choose a tool:", options)

    if choice == "Chemical Calculator":
        chemical_calculator()
    elif choice == "Unit Converter":
        unit_converter()
    elif choice == "Fertilizer Mixer":
        fertilizer_mixer()
    elif choice == "Water Requirements":
        water_requirements()
    elif choice == "Dashboard":
        dashboard()


if __name__ == "__main__":
    main()
