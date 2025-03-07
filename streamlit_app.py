import streamlit as st
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

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

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("❤️ Video")
        idvid = str(df[df["title"] == selected_title]['url'].iloc[0]).split("v=")[1]
        video_url = f'https://www.youtube.com/embed/{idvid}'

        st.markdown(
            f"""
            <iframe width="320" height="180" src="{video_url}" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
            </iframe>
            """,
            unsafe_allow_html=True
        )
        

    with col2:
        st.subheader("📊 Views Over Time")
        fig1 = px.line(filtered_df, x="data_created_at", y="views_count",
                    title=f"Views Count Over Time for {selected_title}", height=180)
        
        # Reduce margins, font sizes, and remove legend to fit small height
        fig1.update_layout(
            margin=dict(l=0, r=0, t=20, b=20),  # Reduce padding
            font=dict(size=10),  # Smaller font
            title=dict(font=dict(size=12)),  # Smaller title
            xaxis=dict(title=None, tickfont=dict(size=8)),  # Smaller x-axis
            yaxis=dict(title=None, tickfont=dict(size=8)),  # Smaller y-axis
            legend=dict(font=dict(size=8), orientation="h")  # Horizontal legend
        )
        st.plotly_chart(fig1, use_container_width=True)

st.title("📊 Youtube Raw Data")

st.data_editor(
    df,
    column_config={
        "title": st.column_config.TextColumn(width="small"),
        "channel_name": st.column_config.TextColumn(width="medium"),
    },
    hide_index=True,
    num_rows="fixed",  # Fix the number of rows displayed
    height=200  # Adjust height to fit 5 rows properly
)

# Row 1: Dim Tables
df_dim_video = conn.query("""
                SELECT 
                    *
                FROM dim_video
                """, ttl="10m")

st.subheader("📁 Dimension Tables")
st.write("🔹 **dim_video**")
# Configure AgGrid options
builder = GridOptionsBuilder.from_dataframe(df_dim_video)
builder.configure_pagination(enabled=True, paginationPageSize=5)  # Set page size to 5
builder.configure_side_bar()  # Enable filter options

# Display the table
AgGrid(df_dim_video, gridOptions=builder.build(), height=200, fit_columns_on_grid_load=True)