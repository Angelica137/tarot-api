import pytest
from unittest.mock import patch, MagicMock
from app.services.spread_service import get_spread_data
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app.models.card_model import Card
from werkzeug.exceptions import NotFound, InternalServerError
from app.services.spread_service import get_spread_data


@pytest.fixture
def mock_spread():
    spread = MagicMock(spec=Spread)
    spread.id = 1
    spread.name = "Test Spread"
    spread.number_of_cards = 3
    spread.to_dict.return_value = {"id": 1, "name": "Test Spread"}
    
    layout = MagicMock(spec=SpreadLayout)
    layout.name = "Test Layout"
    layout.layout_description = ["Position 1", "Position 2", "Position 3"]
    
    spread.layout = layout
    return spread

@pytest.fixture
def mock_card():
    card = MagicMock(spec=Card)
    card.to_dict.return_value = {"id": 1, "name": "Test Card"}
    return card

@patch('app.services.spread_service.get_spread')
@patch('app.services.spread_service.generate_random_cards')
def test_get_spread_data_simple(mock_generate_random_cards, mock_get_spread, mock_spread, mock_card):
    mock_get_spread.return_value = mock_spread
    mock_generate_random_cards.return_value = [mock_card] * 3

    result = get_spread_data(1)

    assert isinstance(result, dict)
    assert "spread" in result
    assert "layout_name" in result
    assert "cards" in result
    assert len(result["cards"]) == 3

    print("Test passed successfully!")


@patch('app.services.spread_service.Spread.query')
def test_get_spread_data_error(mock_query, test_app):
    with test_app.app_context():
        # Mock the query behavior to return None (simulating not found)
        mock_query.get.return_value = None

        with pytest.raises(InternalServerError) as exc_info:
            get_spread_data(999)  # Assume 999 is an ID that doesn't exist
        
        assert "Error getting spread data: 404 Not Found: Spread not found" in str(exc_info.value)

    print("Error test passed successfully!")