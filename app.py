import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="HSA Product Search", layout="wide")

# Correct dataset ID
DATASET_ID = "d_767279312753558cbf19d48344577084"
API_URL = f"https://data.gov.sg/api/action/datastore_search?resource_id={DATASET_ID}&limit=10000"

@st.cache_data
def load_data():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    data = resp.json()
    records = data["result"]["records"]
    return pd.DataFrame(records)

st.title("🔍 HSA Therapeutic Products")

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

st.write(f"Total rows: {len(df)}")
st.write("Columns:", df.columns.tolist())

query = st.text_input("Search term (e.g., product name, ingredient, manufacturer):")

if query:
    filtered = df[df.astype(str).apply(lambda col: col.str.contains(query, case=False)).any(axis=1)]
    st.success(f"Found {len(filtered)} results")
    st.dataframe(filtered, use_container_width=True)
else:
    st.info("Start typing to search")
