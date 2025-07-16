import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="HSA Therapeutic Product Search", layout="wide")

API_URL = "https://data.gov.sg/api/action/datastore_search?resource_id=f1f3e1d2-5a8e-4f3e-a285-d7df57a6dcaf&limit=10000"

@st.cache_data
def load_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    records = data['result']['records']
    df = pd.DataFrame(records)
    return df

st.title("🔍 HSA Therapeutic Product Register")

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

query = st.text_input("Search by product name, active ingredient, or manufacturer:")

if query:
    filtered = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False), axis=1)]
    st.success(f"Found {len(filtered)} result(s):")
    # Show only useful fields
    st.dataframe(filtered[[
        "product_name",
        "active_ingredients",
        "license_holder",
        "manufacturer",
        "route_of_administration",
        "dosage_form",
        "country_of_manufacturer"
    ]], use_container_width=True)
else:
    st.info("Enter a keyword above to search listings.")
