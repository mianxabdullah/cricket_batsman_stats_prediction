import pandas as pd
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

