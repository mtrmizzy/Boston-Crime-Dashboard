# pip install streamlit-folium
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Boston Crime Dashboard", layout="wide")

# --- Title ---
st.title("Boston Crime Dashboard")
st.markdown("Analyze crime trends across Boston (2017–2022) with historical context.")

# --- Sidebar Controls ---
st.sidebar.header("🔧 Dashboard Controls")

# --- Tab Setup ---
tab1, tab2, tab3 = st.tabs(["🗺️ Maps", "📊 District Analysis", "🏙️ Redlining Analysis"])

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("boston_crime.csv")
    return df

df = load_data()

# --- Apply Filters ---
filtered_df = df.copy()

if time_period == "Pre-COVID (2017–2019)":
    filtered_df = filtered_df[filtered_df["YEAR"] < 2020]
elif time_period == "Post-COVID (2020–2022)":
    filtered_df = filtered_df[filtered_df["YEAR"] >= 2020]

if district != "All":
    filtered_df = filtered_df[filtered_df["DISTRICT"] == district]

# ---Display Maps ---
with tab1:
    st.subheader("Crime Map")

    map_object = create_map(filtered_df)  # your existing folium function
    st_folium(map_object, width=700)

def create_map(data):
    mean_lat = data['Lat'].mean()
    mean_long = data['Long'].mean()

    m = folium.Map(location=[mean_lat, mean_long], zoom_start=12)

    heat_data = [[row['Lat'], row['Long']] for _, row in data.iterrows()]

    HeatMap(heat_data, radius=8, blur=5).add_to(m)

    return m

# --- Bar Plots ---
fig = px.bar(
    x=district_counts.index,
    y=district_counts.values,
    labels={'x': 'District', 'y': 'Crime Count'},
    title="Crime Count by District"
)

st.plotly_chart(fig, use_container_width=True)

# --- Redlining Tab ---
with tab3:
    st.subheader("Crime vs Historical Redlining")

    redlining_map = create_redlining_map(filtered_df)
    st_folium(redlining_map, width=700)

    st.markdown("""
    **Insight:**
    We observe overlap between historically redlined areas and higher crime density.
    This may reflect long-term structural inequalities rather than direct causation.
    """)


# # Time period filter
# time_period = st.sidebar.radio(
#     "Select Time Period:",
#     ["All", "Pre-COVID (2017–2019)", "Post-COVID (2020–2022)"]
# )

# # District filter
# district = st.sidebar.selectbox(
#     "Select District:",
#     ["All"]  # placeholder until your real data comes in
# )

# # --- Placeholder for Data ---
# st.subheader("📊 Dashboard Preview")

# st.info("Waiting for cleaned dataset... visualizations will appear here.")
