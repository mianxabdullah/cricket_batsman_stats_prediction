import pandas as pd
import os
def load_kaggle_dataset(data_dir='data'):
    bat_path = os.path.join(data_dir, 'bat.csv')    
    if not os.path.exists(bat_path):
        return None
    df = pd.read_csv(bat_path)
    df_processed = pd.DataFrame()
    df_processed['Player'] = df['name_x']
    df_processed['Opposition'] = df['name_y'] if 'name_y' in df.columns else 'Unknown'
    df_processed['Venue'] = df['title'] if 'title' in df.columns else 'Unknown'
    df_processed['Format'] = df['matchtype'].str.upper() if 'matchtype' in df.columns else 'ODI'
    df_processed['Date'] = pd.to_datetime(df['start_date'], errors='coerce') if 'start_date' in df.columns else pd.NaT
    df_processed['Runs'] = df['runs_x'].fillna(0).astype(int)
    df_processed['Balls'] = df['balls'].fillna(1).astype(int)
    df_processed['4s'] = df['fours'].fillna(0).astype(int)
    df_processed['6s'] = df['sixes'].fillna(0).astype(int)
    df_processed['Out'] = df['how_out'].notna()
    df_processed['Innings'] = df['order'].fillna(1).astype(int)
    df_processed = df_processed[df_processed['Player'].notna() & (df_processed['Player'] != '')]
    df_processed = df_processed[df_processed['Balls'] > 0]
    df_processed = df_processed.drop_duplicates()
    return df_processed
def load_data(filepath='data/mock_cricket_data.csv'):
    if not os.path.exists(filepath):
        return None
    df = pd.read_csv(filepath)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

def preprocess_data(df):
    df = df.dropna(subset=['Player', 'Runs', 'Balls'])
    if 'StrikeRate' not in df.columns and 'Runs' in df.columns and 'Balls' in df.columns:
        df['StrikeRate'] = (df['Runs'] / df['Balls']) * 100
        df['StrikeRate'] = df['StrikeRate'].fillna(0)        
    return df



