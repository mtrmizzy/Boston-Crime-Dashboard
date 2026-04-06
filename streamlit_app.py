import streamlit as st
import pandas as pd
from folium.plugins import HeatMap
import plotly.express as px
import folium
from streamlit_folium import st_folium

# --- Page Config ---
st.set_page_config(page_title="Boston Crime Dashboard", layout="wide")

# --- Title ---
st.title("Boston Crime Dashboard")
st.markdown("Exploring crime patterns across Boston before and after COVID, with historical redlining context.")

# --- Load Data ---
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1QvcPHwJxNmlA6sHBEyqlgzE5SmgjVVkU"
    df = pd.read_csv(url)
    return df

df = load_data()

# --- Sidebar Controls ---
st.sidebar.header("🔧 Dashboard Controls")

time_period = st.sidebar.selectbox(
    "Select Time Period",
    ["All", "Pre-COVID (2017–2019)", "Post-COVID (2020–2022)"]
)

# --- Apply Filters ---
filtered_df = df.copy()

if time_period == "Pre-COVID (2017–2019)":
    filtered_df = filtered_df[filtered_df["YEAR"] < 2020]
elif time_period == "Post-COVID (2020–2022)":
    filtered_df = filtered_df[filtered_df["YEAR"] >= 2020]
else:
    filtered_df = df

# --- Tab Setup ---
tab1, tab2, tab3 = st.tabs([
    "🗺️ Maps", 
    "📊 District Analysis", 
    "🏙️ Redlining Analysis"
])

# --- Map Function ---
def create_map(data):
    mean_lat = data['Lat'].mean()
    mean_long = data['Long'].mean()

    BostonMap = folium.Map(location=[mean_lat, mean_long], zoom_start=12)

    heat_data = [
        [row['Lat'], row['Long'], 1]  # weight = 1 (or use severity if available)
        for _, row in data.iterrows()
    ]

    HeatMap(heat_data,
        radius=8,        # smaller radius = more detail
        blur=5,          # less smoothing
        max_zoom=13
    ).add_to(BostonMap)

    # District Centers
    district_locations = data.groupby('DISTRICT')[['Lat', 'Long']].mean().reset_index()

    # District Counts
    district_counts = data['DISTRICT'].value_counts().reset_index()
    district_counts.columns = ['DISTRICT', 'count']

    # Merge the two District data
    district_data = district_locations.merge(district_counts, on='DISTRICT')

    # Plot Visual
    for _, row in district_data.iterrows():
        folium.CircleMarker(
            location=[row['Lat'], row['Long']],
            radius=row['count'] / 500,  # scale size
            color='blue',
            fill=True,
            fill_opacity=0.6,
            tooltip=f"District {row['DISTRICT']} | Crimes: {row['count']}"
        ).add_to(BostonMap)
    
    return BostonMap

# --- Get Color Function ---
def get_color(grade):
    color_map = {
        'A': '#2ECC71',  # green
        'B': '#3498DB',  # blue
        'C': '#F1C40F',  # yellow
        'D': '#E74C3C'   # red
    }
    return color_map.get(grade, 'gray')  # fallback if something unexpected appears

# # --- Redlining Map Function ---
# def create_redlining_map(data):
#     mean_lat = data['Lat'].mean()
#     mean_long = data['Long'].mean()

#     BostonMap = folium.Map(location=[mean_lat, mean_long], zoom_start=11)

#     folium.GeoJson(
#         "boston_redlining.json",
#         name="Redlining Zones",
#         style_function=lambda feature: {
#             'fillColor': get_color(feature['properties']['grade']),
#             'color': 'black',
#             'weight': 1,
#             'fillOpacity': 0.3
#         },
#         tooltip=folium.GeoJsonTooltip(
#             fields=['grade'],
#             aliases=['HOLC Grade:']
#         )
#     ).add_to(BostonMap)

#     return BostonMap
    
# ---Display Maps ---
with tab1:
    st.subheader("Crime Map")

    map_object = create_map(filtered_df)  # your existing folium function
    st_folium(map_object, width=700)

    st.markdown("""
    **Insight:** Crime is geographically concentrated and remains consistent across time periods.
    """)

# --- Bar Plots ---
with tab2:
    st.subheader('Crime Count by District')
    
    district_counts = (
        filtered_df['DISTRICT']
        .value_counts()
        .sort_values(ascending=False)
    )
    
    fig = px.bar(
        x=district_counts.index,
        y=district_counts.values,
        labels={'x': 'District', 'y': 'Crime Count'},
        title="Crime Count by District"
    )

    # Rotate x-axis labels properly
    fig.update_layout(
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:** Certain districts consistently report higher crime levels.
    """)

# # --- Redlining Map Overlay Tab ---
# with tab3:
#     st.subheader("Redlining & Crime Overlay")

#     red_map = create_redlining_map(filtered_df)
#     st_folium(red_map, width=1000, height=600)

#     st.markdown("""
#     **Insight:** Areas historically graded lower (redlined) show higher modern crime density.

#     ⚠️ This reflects long-term structural inequality, not direct causation.
#     """)
