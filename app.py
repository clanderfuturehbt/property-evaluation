
# Production-Ready Property Evaluation Model with External Data and Streamlit UI

import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# === External Data Functions ===

def get_census_data(state_fips, county_fips, api_key):
    base_url = "https://api.census.gov/data/2021/acs/acs5"
    params = {
        "get": "NAME,B19013_001E",
        "for": f"county:{county_fips}",
        "in": f"state:{state_fips}",
        "key": api_key
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[1][1]
    except requests.RequestException as e:
        st.error(f"Error fetching Census data: {e}")
        return "N/A"

def get_zillow_rent_zestimate(property_address, zillow_api_key):
    st.warning("Zillow API integration requires approval and setup. Returning sample value.")
    return 2500

st.set_page_config(page_title="Property Evaluation Dashboard", layout="wide")
st.title("🏢 Property Evaluation Model with External Data")

st.sidebar.header("🔑 API Key Management")

census_api_key = st.sidebar.text_input("U.S. Census API Key", type="password", value=os.getenv("CENSUS_API_KEY", ""))
zillow_api_key = st.sidebar.text_input("Zillow API Key", type="password", value=os.getenv("ZILLOW_API_KEY", ""))

st.header("1️⃣ Property Relations")
col1, col2 = st.columns(2)
with col1:
    discovery = st.text_input("Discovery")
    validation = st.text_input("Validation")
with col2:
    creation = st.text_input("Creation")
    relationship = st.text_input("Relationship")

st.header("2️⃣ Property Evaluation")
col1, col2 = st.columns(2)
with col1:
    zoning = st.text_input("Zoning")
    permitting = st.text_input("Permitting Process")
    gov_programs = st.text_area("Government Programs (comma-separated)").split(",")
    improvement_districts = st.text_area("Improvement Districts (comma-separated)").split(",")
    cost_per_sqft = st.number_input("Cost per Sq Ft", min_value=0, value=200)
    demographics = st.text_input("Demographics")

with col2:
    st.subheader("Fetch External Data")
    state_fips = st.text_input("State FIPS Code")
    county_fips = st.text_input("County FIPS Code")

    if st.button("Get Census Median Income"):
        avg_income = get_census_data(state_fips, county_fips, census_api_key)
        st.success(f"Median Household Income: ${avg_income}")
    else:
        avg_income = 85000

    property_address = st.text_input("Property Address")
    if st.button("Get Zillow Rent Zestimate"):
        avg_dwelling_price_rent = get_zillow_rent_zestimate(property_address, zillow_api_key)
        st.success(f"Zillow Rent Zestimate: ${avg_dwelling_price_rent}")
    else:
        avg_dwelling_price_rent = 2500

avg_dwelling_price_own = st.number_input("Avg Dwelling Price (Own)", min_value=0, value=350000)
occupancy_rates = st.slider("Occupancy Rates (%)", 0, 100, 92)
net_migration = st.text_input("Net Migration (UHaul index)")

st.header("3️⃣ Estimating Model")
bldg_sqft = st.number_input("Building Sq Ft", min_value=0, value=50000)
units_by_type_input = st.text_area("Units by Type (format: 1BR:20,2BR:15)").split(",")

units_by_type_dict = {}
for item in units_by_type_input:
    if ":" in item:
        key, val = item.split(":")
        try:
            units_by_type_dict[key.strip()] = int(val.strip())
        except ValueError:
            st.warning(f"Invalid value for {key.strip()}: {val.strip()}")

commercial_units = st.number_input("Commercial Units", min_value=0, value=3)
conversion_costs = st.number_input("Conversion Costs", min_value=0, value=3000000)
rental_income = st.number_input("Rental Income", min_value=0, value=1200000)
operating_expenses = st.number_input("Operating Expenses", min_value=0, value=400000)
condo_sellout = st.number_input("Total Condo Sell-Out", min_value=0, value=20000000)

if st.button("Evaluate Property"):
    total_cost = (bldg_sqft * cost_per_sqft) + conversion_costs
    noi = rental_income - operating_expenses
    profit = condo_sellout - total_cost
    roi = (profit / total_cost) * 100 if total_cost else 0

    st.success("✅ Evaluation Complete")

    st.metric("Total Development Cost", f"${total_cost:,.2f}")
    st.metric("Net Operating Income (NOI)", f"${noi:,.2f}")
    st.metric("For-Sale ROI", f"{roi:.2f}%")

    st.markdown("---")
    st.subheader("📊 Unit Mix Summary")
    for unit, count in units_by_type_dict.items():
        st.write(f"{unit}: {count} units")

st.markdown("---")
st.caption("© 2025 Property Evaluation Tool. Built with ❤️ using Streamlit")
