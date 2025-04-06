from unittest.mock import patch
from player import Player


@patch('player.players.get_players')
def test_get_player_id_valid(mock_get_players):
    mock_get_players.return_value = [{'full_name': 'LeBron James', 'id': 2544}]
    player = Player('LeBron James', '2023-24')
    assert player.get_player_id_by_name() == 2544

@patch('player.players.get_players')
def test_get_player_id_invalid(mock_get_players):
    mock_get_players.return_value = [{'full_name': 'Stephen Curry', 'id': 201939}]
    player = Player('Wrong Guy', '2023-24')
    assert player.get_player_id_by_name() is None

@patch('player.playerprofilev2.PlayerProfileV2')
@patch('player.Player.get_player_id_by_name', return_value=2544)
def test_get_stats_success(mock_id, mock_profile):
    mock_profile.return_value.get_normalized_dict.return_value = {
        "SeasonTotalsRegularSeason": [{
            "SEASON_ID": "2023-24",
            "PTS": 27.2,
            "AST": 6.0,
            "FG_PCT": 0.51,
            "FG3_PCT": 0.39,
            "FT_PCT": 0.75,
            "DREB": 7.5,
            "STL": 1.2,
            "BLK": 0.6
        }]
    }
    player = Player("LeBron James", "2023-24")
    stats = player.get_stats()
    assert stats["Points"] == 27.2
    assert stats["FG3 %"] == 0.39

@patch('player.Player.get_player_id_by_name', return_value=None)
def test_get_stats_invalid_player(mock_id):
    player = Player("Fake Name", "2023-24")
    assert player.get_stats() is None
