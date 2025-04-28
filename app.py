import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# Set page config
st.set_page_config(
    page_title="Swiggy Restaurant Recommender 🍽️",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to create stars
def display_stars(rating):
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    stars = '⭐' * full_stars
    if half_star:
        stars += '⭐'
    return stars

# Load data
cleaned_data = pd.read_csv('cleaned_data.csv')
encoded_data = pd.read_csv('encoded_data.csv')
with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# 1. Sidebar Filters
st.sidebar.title("🎯 Filters")

city_filter = st.sidebar.selectbox("Select City", options=["All"] + sorted(cleaned_data['city'].unique()))
cuisine_filter = st.sidebar.selectbox("Select Cuisine", options=["All"] + sorted(cleaned_data['cuisine'].unique()))
min_rating = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=5.0, step=0.5, value=3.0)

# ✅ Price Range Slider (Between Min & Max)
price_range = st.sidebar.slider(
    "Select Price Range (₹)",
    min_value=int(cleaned_data['cost'].min()),
    max_value=int(cleaned_data['cost'].max()),
    value=(100, 1000)  # Default range you can adjust
)

# Apply Filters
filtered_data = cleaned_data.copy()
if city_filter != "All":
    filtered_data = filtered_data[filtered_data['city'] == city_filter]
if cuisine_filter != "All":
    filtered_data = filtered_data[filtered_data['cuisine'] == cuisine_filter]

filtered_data = filtered_data[
    (filtered_data['rating'] >= min_rating) &
    (filtered_data['cost'] >= price_range[0]) & 
    (filtered_data['cost'] <= price_range[1])
]


# 2. Main Title
st.title("🍴 Swiggy's Restaurant Recommendation System")

# 3. Recommendation Methodology
st.subheader("🔍 Recommended Restaurants For You")

# Check if enough data to sample
if len(filtered_data) >= 5:
    recommendations = filtered_data.sample(5)
else:
    recommendations = filtered_data

# 4. Display Recommended Restaurants
if not recommendations.empty:
    for index, row in recommendations.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="background-color:#f0f2f6; padding:15px; border-radius:15px; margin-bottom:15px">
                <h3 style="color:#F63366;">{row['name']}</h3>
                <p><b>📍 City:</b> {row['city']}</p>
                <p><b>🍽️ Cuisine:</b> {row['cuisine']}</p>
                <p><b>⭐ Rating:</b> {display_stars(row['rating'])} ({row['rating']})</p>
                <p><b>💰 Cost for Two:</b> ₹{row['cost']}</p>
                <p><b>📜 Address:</b> {row['address']}</p>
                <a href="{row['link']}" target="_blank" style="color:blue; font-weight:bold;">🔗 View on Swiggy</a>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.warning(" No restaurants found matching your filters. Try changing filters!")

# Footer
st.markdown("---")
st.markdown("Made with  by Maheshprasad K R | Powered by Streamlit 🚀")
