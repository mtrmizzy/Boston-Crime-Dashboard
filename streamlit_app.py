import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="Boston Crime Dashboard", layout="wide")

# --- Title ---
st.title("Boston Crime Dashboard")
st.markdown("Analyze crime trends across Boston (2017–2022) with historical context.")

# --- Sidebar Controls ---
st.sidebar.header("🔧 Dashboard Controls")

# Time period filter
time_period = st.sidebar.radio(
    "Select Time Period:",
    ["All", "Pre-COVID (2017–2019)", "Post-COVID (2020–2022)"]
)

# District filter
district = st.sidebar.selectbox(
    "Select District:",
    ["All"]  # placeholder until your real data comes in
)

# --- Placeholder for Data ---
st.subheader("📊 Dashboard Preview")

st.info("Waiting for cleaned dataset... visualizations will appear here.")
