import streamlit as st
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("🎬 YouTube Views Tracker")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query("""
                SELECT 
                    data_created_at, 
                    title, 
                    channel_name, 
                    views_count, 
                    likes_count, 
                    comments_count, 
                    upload_date,
                    url
                FROM raw_youtube_data
                """, ttl="10m")

last_updated = df["data_created_at"].max()


st.markdown(f"""🚀 Curious about how a YouTube video performs? See its view trends, updated every **5 minutes**!  
📅 **Last Updated:** {last_updated}""")


# Dropdown for Title Selection
unique_titles = df["title"].unique()
selected_title = st.selectbox("Select a Title", unique_titles)

# Filter Data based on selected Title
filtered_df = df[df["title"] == selected_title]