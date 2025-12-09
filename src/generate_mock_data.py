import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_mock_data(num_rows=500):
    players = ['Babar Azam', 'Virat Kohli', 'Joe Root', 'Steve Smith', 'Kane Williamson', 'Rohit Sharma', 'David Warner', 'Jos Buttler']
    teams = ['Pakistan', 'India', 'England', 'Australia', 'New Zealand']
    venues = ['MCG', 'Lords', 'Eden Gardens', 'Dubai International Stadium', 'Old Trafford']
    formats = ['T20I', 'ODI', 'Test']


