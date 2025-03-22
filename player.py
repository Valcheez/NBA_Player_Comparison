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
                
    # def compare_season_stats(self, player2):
    #     """Compares the stats of the two players"""

    #     player1_stats = self.get_stats()
    #     player2_stats = player2.get_stats()

    #     if player1_stats is None or player2_stats is None:
    #         print("Error: Cannot compare stats.")
    #         return
        
    #     for key in player1_stats:
    #         if key in player2_stats:
    #             if player1_stats[key] > player2_stats[key]:
    #                 print(f"{player1_name} has greater '{key}': {player1_stats[key]}")
    #             elif player1_stats[key] < player2_stats[key]:
    #                 print(f"{player2_name} has greater '{key}': {player2_stats[key]}")
    #             else:
    #                 print(f"{player1_name} and {player2_name} have equal value for key {key}")
                

                   
# player1_name = input("Enter the player's full name: ").strip()
# if not player1_name:
#     print("Error: Player name cannot be empty.")
#     exit()
# player1_season = input("Enter the season year(e.g., '2023-24'): ").strip()
# if not re.match(r'^\d{4}-\d{2}$', player1_season):
#     print("Error: Season year is not in the correct format (e.g., '2022-23').")
#     exit()

# player1_name = "Lebron James"
# player1_season = "2020-21"
# nba_player1 = Player(player1_name, player1_season)
# nba_player1.get_player_id_by_name()


# player2_name = input("Enter the second player's full name: ").strip()
# player2_season = input("Enter the season year: ").strip()

# player2_name = "Stephen Curry"
# player2_season = "2020-21"
# nba_player2 = Player(player2_name, player2_season)
# nba_player2.get_player_id_by_name()

# Compares offensive stats
# nba_player1.compare_season_stats(nba_player2)