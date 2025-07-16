import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="Singapore Data Search Tool", layout="wide")

# 🔁 Replace this with your actual CSV download link
CSV_URL = "https://www.data.gov.sg/api/action/datastore_search?resource_id=d_767279312753558cbf19d48344577084"

@st.cache_data
def load_data():
    # Try reading CSV directly if it's a link to CSV file
    if CSV_URL.endswith(".csv"):
        df = pd.read_csv(CSV_URL)
    else:
        # If it's a data.gov.sg API endpoint, fetch records
        response = requests.get(CSV_URL)
        data = response.json()
        records = data['result']['records']
        df = pd.DataFrame(records)
    return df

st.title("🔍 Singapore Open Data Search")

try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

query = st.text_input("Search for a keyword in the dataset:")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False), axis=1)]
    st.success(f"Found {len(results)} result(s):")
    st.dataframe(results, use_container_width=True)
else:
    st.info("Enter a keyword to search listings.")
