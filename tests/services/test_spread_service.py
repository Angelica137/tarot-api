import pytest
from app.services.spread_service import get_spread, get_spread_data
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from werkzeug.exceptions import NotFound, InternalServerError


def test_get_spread_success(test_app, session):
    with test_app.app_context():
        # Create a sample spread and layout
        layout = SpreadLayout(name="Test Layout", layout_description='{"type": "linear"}')
        spread = Spread(name="Test Spread", number_of_cards=3, layout=layout)
        session.add(layout)
        session.add(spread)
        session.commit()

        # Call the function
        result = get_spread(spread.id)

        # Assert the result
        assert isinstance(result, Spread)
        assert result.id == spread.id
        assert result.name == "Test Spread"
        assert result.number_of_cards == 3
        assert result.layout.name == "Test Layout"


def test_get_spread_not_found(test_app):
    with test_app.app_context():
        # Call the function and check if it raises NotFound
        with pytest.raises(NotFound):
            get_spread(999)  # Assume 999 is an ID that doesn't exist


def test_get_spread_data_success(test_app, session):
    with test_app.app_context():
        # Create a sample spread and layout
        layout = SpreadLayout(name="Test Layout", layout_description='{"type": "linear"}')
        spread = Spread(name="Test Spread", number_of_cards=3, layout=layout)
        session.add(layout)
        session.add(spread)
        session.commit()

        # Call the function
        result = get_spread_data(spread.id)

        # Assert the result
        assert isinstance(result, dict)
        assert result['id'] == spread.id
        assert result['name'] == "Test Spread"
        assert result['number_of_cards'] == 3
        assert result['layout']['name'] == "Test Layout"
        assert result['layout']['description'] == '{"type": "linear"}'


def test_get_spread_data_error(test_app):
    with test_app.app_context():
        with pytest.raises(InternalServerError):
            get_spread_data(999)  # Assume 999 is an ID that doesn't exist
