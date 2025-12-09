import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_mock_data(num_rows=500):
    players = ['Babar Azam', 'Virat Kohli', 'Joe Root', 'Steve Smith', 'Kane Williamson', 'Rohit Sharma', 'David Warner', 'Jos Buttler']
    teams = ['Pakistan', 'India', 'England', 'Australia', 'New Zealand']
    venues = ['MCG', 'Lords', 'Eden Gardens', 'Dubai International Stadium', 'Old Trafford']
    formats = ['T20I', 'ODI', 'Test']

    data = []
    start_date = datetime(2015, 1, 1)
    for _ in range(num_rows):
        player = random.choice(players)
        opposition = random.choice([t for t in teams if t != 'India'])
        venue = random.choice(venues)
        match_format = random.choice(formats)
        date = start_date + timedelta(days=random.randint(0, 3000))
        
        if match_format == 'T20I':
            balls = random.randint(0, 60)
            runs = int(balls * random.uniform(0.5, 2.5)) if balls > 0 else 0
            fours = int(runs / 10)
            sixes = int(runs / 20)
        elif match_format == 'ODI':
            balls = random.randint(0, 150)
            runs = int(balls * random.uniform(0.4, 1.5)) if balls > 0 else 0
            fours = int(runs / 12)
            sixes = int(runs / 30)
        else: # Test
            balls = random.randint(0, 300)
            runs = int(balls * random.uniform(0.2, 0.8)) if balls > 0 else 0
            fours = int(runs / 15)
            sixes = int(runs / 50)
