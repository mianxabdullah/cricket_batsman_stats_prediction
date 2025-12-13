import pandas as pd
import numpy as np
def get_player_stats(df, player_name):
    player_df = df[df['Player'] == player_name]
    if player_df.empty:
        return None
    stats = {
        'Matches': len(player_df),
        'Runs': player_df['Runs'].sum(),
        'Average': player_df['Runs'].mean(),
        'Strike Rate': (player_df['Runs'].sum() / player_df['Balls'].sum()) * 100 if player_df['Balls'].sum() > 0 else 0,
        '100s': len(player_df[player_df['Runs'] >= 100]),
        '50s': len(player_df[(player_df['Runs'] >= 50) & (player_df['Runs'] < 100)]),
        '4s': player_df['4s'].sum(),
        '6s': player_df['6s'].sum(),
        'Highest Score': player_df['Runs'].max()
    }
    return stats

def get_format_stats(df, player_name):
    player_df = df[df['Player'] == player_name]

    stats = player_df.groupby('Format').agg(
        Runs=('Runs', 'sum'),
        Balls=('Balls', 'sum'),
        Fours=('4s', 'sum'),
        Sixes=('6s', 'sum'),
        Highest_Score=('Runs', 'max'),
        Hundreds=('Runs', lambda x: (x >= 100).sum()),
        Fifties=('Runs', lambda x: ((x >= 50) & (x < 100)).sum())
    ).reset_index()

    stats['Strike_Rate'] = np.where(
        stats['Balls'] > 0,
        (stats['Runs'] / stats['Balls']) * 100,
        0
    )
    return stats

