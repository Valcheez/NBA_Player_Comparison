import pytest
import nba_api
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'NBA Player Regular Season Comparison' in response.data

def test_empty_form_submission(client):
    response = client.post('/compare', data={}, follow_redirects=True)
    assert b'Player 1 name is required.' in response.data
    assert b'Player 2 name is required.' in response.data
    assert b'Player 1 season is required.' in response.data
    assert b'Player 2 season is required.' in response.data


@patch('app.Player.get_stats')
def test_invalid_player_entry(mock_get_stats, client):
    # Simulate the first player not found (returns None), second one returns valid stats
    mock_get_stats.side_effect = [None, {'Points': 30}]
    
    response = client.post('/compare', data={
        'player1': 'Not A Real Player',
        'player1_season': '2023-24',
        'player2': 'Stephen Curry',
        'player2_season': '2023-24'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Could not retrieve stats for one or both players' in response.data

def test_invalid_season_format(client):
    response = client.post('/compare', data={
        'player1': 'LeBron James',
        'player1_season': '2023',
        'player2': 'Stephen Curry',
        'player2_season': '2023-24'
    }, follow_redirects=True)
    assert b'season must be in YYYY-YY format' in response.data

def test_reset_redirects_home(client):
    response = client.get('/reset', follow_redirects=True)
    assert b'NBA Player Regular Season Comparison' in response.data
