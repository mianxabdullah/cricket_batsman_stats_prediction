import streamlit as st
import pandas as pd
import os
from src.data_loader import load_data,load_kaggle_dataset

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