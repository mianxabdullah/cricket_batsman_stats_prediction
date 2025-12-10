import streamlit as st
import pandas as pd
import os
from src.data_loader import load_data,load_kaggle_dataset,preprocess_data
from src.eda import get_player_stats, get_format_stats
from src.model import ScorePredictor

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

    elif page == "Performance Prediction (ML)":
        st.header("Match Score Prediction")
        st.markdown("Predict a player's score in the next match using Regression Analysis.")
        
        selected_player_ml = st.selectbox("Select Player for Prediction", players)
        predictor = ScorePredictor()
        
        with st.spinner("Training model on player data..."):
            mae = predictor.train(df)
        
        st.success(f"Model Trained! Mean Absolute Error on Test Set: {mae:.2f} runs")  
        st.subheader("Predict Next Match Score")
        
        col1, col2 = st.columns(2)
        
        player_df = df[df['Player'] == selected_player_ml].sort_values('Date')
        recent_avg_default = player_df['Runs'].tail(5).mean() if len(player_df) >= 5 else 30.0
        
        with col1:
            recent_form = st.number_input("Recent Batting Average (Last 5 Matches)", value=float(recent_avg_default))
        
        with col2:
            venue_avg = st.number_input("Historical Average at Venue", value=35.0)
            
        if st.button("Predict Score"):
            prediction = predictor.predict(recent_form, venue_avg)
            st.balloons()
            st.metric(label="Predicted Runs", value=f"{int(prediction)}")
            
            if prediction > 50:
                st.info("The model predicts a strong performance! Likely a 50+ score.")
            elif prediction < 20:
                st.warning("The model predicts a tough inning. Early wicket risk.")
else:
    st.info("Please load data to proceed.")
