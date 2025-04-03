from nba_api.stats.endpoints import playerprofilev2
from nba_api.stats.library.data import players
from nba_api.stats.static import players
import re


class Player:

    def __init__(self, player_name, season_year):
        self.player_name = player_name
        self.season_year = season_year

    def get_player_id_by_name(self):
        """Retrieve a player ID by their full name."""

        all_players = players.get_players()
        for player in all_players:
            if player['full_name'].lower() == self.player_name.lower():
                # print(player['id'])
                return player['id']
        print(f"Error: Player '{self.player_name}' not found.")
        return None

    def get_stats(self):
        """Retrieves a player's stats"""

        try:
            player_id = self.get_player_id_by_name()
            if not player_id:
                return None
            
            player_profile = playerprofilev2.PlayerProfileV2(self.get_player_id_by_name())
            data = player_profile.get_normalized_dict()   # data is the dictionary
        
        except Exception as e:
            print(f"An error occurred: {e}")

        if "SeasonTotalsRegularSeason" in data:
            season_data = data["SeasonTotalsRegularSeason"]
            for row in season_data:
                if self.season_year == row["SEASON_ID"]:
                    Stats = {"Points": row["PTS"], "Assists": row["AST"], "FG %": row["FG_PCT"], "FG3 %": row["FG3_PCT"], "FT %": row["FG_PCT"], "DREB": row["DREB"], "Steals": row["STL"], "Blocks": row["BLK"]}
                    print(Stats)
                    return Stats
        else:
            print(f"Error: No data found for the season '{self.season_year}' for player '{self.player_name}'.")
            return None
        
                

            