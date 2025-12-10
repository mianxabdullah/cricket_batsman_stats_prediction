import streamlit as st
import pandas as pd
import os
from src.data_loader import load_data,load_kaggle_dataset,preprocess_data
from src.eda import get_player_stats, get_format_stats

st.set_page_config(
    page_title="Cricket Performance Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)
def load_css():
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.title("🏏 Cricket Player Performance Analysis")
st.markdown("### Advanced Analytics & Performance Prediction Tool")

st.sidebar.header("Configuration")
data_source = st.sidebar.radio("Data Source", ["Mock Data", "Kaggle Dataset", "Upload CSV"])

df = None
if data_source == "Mock Data":
    if os.path.exists("data/mock_cricket_data.csv"):
        df = load_data("data/mock_cricket_data.csv")
        st.sidebar.success("Mock Data Loaded Successfully")
    else:
        st.sidebar.error("Mock data not found. Please run generation script.")

elif data_source == "Kaggle Dataset":
    df = load_kaggle_dataset("data")
    if df is not None:
        st.sidebar.success(f"✅ Kaggle Dataset Loaded: {len(df)} records")
        st.sidebar.info(f"📊 Players: {df['Player'].nunique()}")
    else:
        st.sidebar.error("Kaggle dataset files not found. Please ensure bat.csv and match.csv are in the data folder.")
else:
    uploaded_file = st.sidebar.file_uploader("Upload Cricket Data CSV", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
if df is not None:
    df = preprocess_data(df)
    page = st.sidebar.selectbox("Navigate", ["Player Profile (EDA)", "Performance Prediction (ML)"])
    players = df['Player'].unique().tolist()
    if page == "Player Profile (EDA)":
        st.header("Player Career Statistics")
        selected_player = st.selectbox("Select Player", players) 
        if selected_player:
            stats = get_player_stats(df, selected_player)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Runs", stats['Runs'])
            col2.metric("Batting Average", f"{stats['Average']:.2f}")
            col3.metric("Strike Rate", f"{stats['Strike Rate']:.2f}")
            col4.metric("Highest Score", stats['Highest Score'])
            
            col5, col6, col7, col8 = st.columns(4)
            col5.metric("Matches", stats['Matches'])
            col6.metric("Centuries (100s)", stats['100s'])
            col7.metric("Half-Centuries (50s)", stats['50s'])
            col8.metric("Boundaries (4s/6s)", f"{stats['4s']} / {stats['6s']}")
            
            st.subheader("Performance by Format")
            format_stats = get_format_stats(df, selected_player)
            st.dataframe(format_stats, use_container_width=True)
            
            st.subheader("Recent Form (Last 10 Innings)")
            player_matches = df[df['Player'] == selected_player].sort_values('Date').tail(10)
            st.line_chart(player_matches.set_index('Date')['Runs'])