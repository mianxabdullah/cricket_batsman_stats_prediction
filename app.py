import streamlit as st
import pandas as pd
import os

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

