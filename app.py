import streamlit as st
import pandas as pd
import numpy as np

def chemical_calculator():
    st.header("Chemical Dosage Calculator")
    st.write("Calculate the required chemical dosage for a specific area.")

    # Input fields
    total_area = st.number_input("Enter total area recommended (e.g., 10 ha):", min_value=0.0, step=0.1)
    total_chemical = st.number_input("Enter total chemical recommended (e.g., 1 L):", min_value=0.0, step=0.01)
    desired_area = st.number_input("Enter your desired area (e.g., 3 ha):", min_value=0.0, step=0.1)

    if st.button("Calculate"):
        if total_area > 0 and total_chemical > 0:
            dosage_per_ha = total_chemical / total_area
            required_chemical = dosage_per_ha * desired_area
            st.success(f"You need {required_chemical:.2f} L of chemical for {desired_area} ha.")
        else:
            st.error("Please enter valid inputs for total area and total chemical.")

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

    if st.button("Convert"):
        if (from_unit, to_unit) in conversion_factors:
            converted_value = value * conversion_factors[(from_unit, to_unit)]
            st.success(f"{value} {from_unit} is equal to {converted_value:.2f} {to_unit}.")
        elif from_unit == to_unit:
            st.info("Units are the same. No conversion needed.")
        else:
            st.error("Conversion not available for the selected units.")

def fertilizer_mixer():
    st.header("Fertilizer Mixing Ratio")
    st.write("Calculate mixing ratios for fertilizers or chemicals.")

    # Input fields
    fertilizer_type = st.selectbox("Select fertilizer type:", ["NPK", "Custom"])
    if fertilizer_type == "Custom":
        total_volume = st.number_input("Enter total chemical volume (L):", min_value=0.0, step=0.01)
        ratio = st.text_input("Enter ratio (e.g., 10:20:10):")
        if st.button("Calculate Ratio"):
            try:
                parts = list(map(int, ratio.split(":")))
                total_parts = sum(parts)
                amounts = [round((part / total_parts) * total_volume, 2) for part in parts]
                st.success(f"Mixing amounts: {amounts} L for ratio {ratio}.")
            except ValueError:
                st.error("Invalid ratio format. Use numbers separated by colons (e.g., 10:20:10).")
    else:
        st.write("Predefined fertilizer ratios coming soon!")

def water_requirements():
    st.header("Water Requirements")
    st.write("Calculate water needed for chemical dilution.")

    # Input fields
    chemical_volume = st.number_input("Enter chemical volume (L):", min_value=0.0, step=0.01)
    dilution_rate = st.number_input("Enter dilution rate (e.g., 1:100):", min_value=0.0, step=0.1)

    if st.button("Calculate Water"):
        if dilution_rate > 0:
            water_volume = chemical_volume * dilution_rate
            st.success(f"You need {water_volume:.2f} L of water to dilute {chemical_volume:.2f} L of chemical.")
        else:
            st.error("Please enter a valid dilution rate.")

def main():
    st.title("Farm Helper: Chemical and Fertilizer Calculator")
    st.sidebar.title("Navigation")
    options = ["Chemical Calculator", "Unit Converter", "Fertilizer Mixer", "Water Requirements"]
    choice = st.sidebar.radio("Choose a tool:", options)

    if choice == "Chemical Calculator":
        chemical_calculator()
    elif choice == "Unit Converter":
        unit_converter()
    elif choice == "Fertilizer Mixer":
        fertilizer_mixer()
    elif choice == "Water Requirements":
        water_requirements()

if __name__ == "__main__":
    main()
