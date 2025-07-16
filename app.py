import streamlit as st
import pandas as pd

st.set_page_config(page_title="HSA Product Search", layout="wide")

# ✅ Replace this with the actual working CSV URL
CSV_URL = "https://datagovsg.github.io/health-supplements-datasets/therapeutic-product-register.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

st.title("🔍 HSA Therapeutic Product Register Search")

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

query = st.text_input("Search by product name, active ingredient, or license holder:")

if query:
    filtered = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False), axis=1)]
    st.success(f"Found {len(filtered)} result(s):")
    # Show only key fields for clarity
    st.dataframe(filtered[["product_name", "active_ingredients", "license_holder", "manufacturer", "route_of_administration"]], use_container_width=True)
else:
    st.info("Type a keyword above to search.")
