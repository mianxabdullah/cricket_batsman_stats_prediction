import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ScorePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def prepare_features(self, df):
        df = df.sort_values(['Player', 'Date'])
        df['RollingAvg_5'] = df.groupby('Player')['Runs'].transform(lambda x: x.rolling(window=5, min_periods=1).mean().shift(1))
        df['VenueAvg'] = df.groupby(['Player', 'Venue'])['Runs'].transform(lambda x: x.expanding().mean().shift(1))
        df = df.fillna(0)       
        return df
        

