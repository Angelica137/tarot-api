import pytest
from app.services.spread_service import get_spread_data
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app.models.card_model import Card
from werkzeug.exceptions import NotFound, InternalServerError
import json


def create_sample_data(session):
    # Create a sample SpreadLayout with the correct structure
    layout = SpreadLayout(
        name="Three Card Spread",
        layout_description=json.dumps(
            {
                "type": "linear",
                "positions": [
                    {"name": "Past", "x": 0, "y": 0},
                    {"name": "Present", "x": 1, "y": 0},
                    {"name": "Future", "x": 2, "y": 0},
                ],
            }
        ),
    )
    session.add(layout)
    session.flush()  # This assigns an ID to layout
    print(f"Created layout with ID: {layout.id}")

    # Create a Spread
    spread = Spread(
        name="Past, Present, Future",
        number_of_cards=3,
        layout=layout,
        position_meanings={
            "Past": "Past events influencing the situation",
            "Present": "Current state of affairs",
            "Future": "Potential outcomes",
        },
    )
    session.add(spread)
    session.flush()  # This assigns an ID to spread
    print(f"Created spread with ID: {spread.id}")

    # Create some Cards
    cards = []
    for i in range(10):  # Create more cards than needed for the spread
        card = Card(
            name=f"Test Card {i}",
            number=str(i),
            arcana="Major" if i % 2 == 0 else "Minor",
            suit="Wands"
            if i % 4 == 0
            else "Cups"
            if i % 4 == 1
            else "Swords"
            if i % 4 == 2
            else "Pentacles",
            img=f"test_image_{i}.jpg",
            fortune_telling=json.dumps([f"Fortune {i}", f"Another fortune {i}"]),
            keywords=json.dumps([f"Keyword {i}", f"Another keyword {i}"]),
            meanings=json.dumps(
                {"light": [f"Light meaning {i}"], "shadow": [f"Shadow meaning {i}"]}
            ),
            archetype=f"Archetype {i}",
            hebrew_alphabet=f"Hebrew {i}",
            numerology=f"Numerology {i}",
            elemental=f"Element {i}",
            mythical_spiritual=f"Myth {i}",
            questions_to_ask=json.dumps([f"Question {i}?", f"Another question {i}?"]),
        )
        session.add(card)
        cards.append(card)

    session.commit()
    print(f"Committed changes. Spread ID: {spread.id}")

    return spread.id


def test_get_spread_data_success(test_app, session):
    with test_app.app_context():
        spread_id = create_sample_data(session)
        print(f"Spread ID returned from create_sample_data: {spread_id}")

        # Call the function
        result = get_spread_data(spread_id)

        # Assert the result
        assert isinstance(result, dict)
        assert "spread" in result  # Ensure 'spread' key exists
        assert "layout_name" in result  # Ensure 'layout_name' key exists
        assert "cards" in result  # Ensure 'cards' key exists

        # Assert 'spread' details
        spread_data = result["spread"]
        assert isinstance(spread_data, dict)
        assert spread_data["id"] == spread_id
        assert spread_data["name"] == "Past, Present, Future"
        assert spread_data["number_of_cards"] == 3
        assert "layout" in spread_data  # Ensure 'layout' key exists

        # Assert 'layout' details
        layout_data = spread_data["layout"]
        assert isinstance(layout_data, dict)
        assert layout_data["name"] == "Three Card Spread"
        assert layout_data["description"] == json.dumps(
            {
                "type": "linear",
                "positions": [
                    {"name": "Past", "x": 0, "y": 0},
                    {"name": "Present", "x": 1, "y": 0},
                    {"name": "Future", "x": 2, "y": 0},
                ],
            }
        )

        # Assert 'cards' structure and details
        assert isinstance(result["cards"], list)
        assert len(result["cards"]) == 3
        for card_data in result["cards"]:
            assert "position" in card_data
            assert isinstance(card_data["position"], int)
            assert "description" in card_data
            assert isinstance(card_data["description"], str)
            assert "card" in card_data
            card = card_data["card"]
            assert "name" in card
            assert "number" in card
            assert "arcana" in card
            assert "suit" in card
            assert "img" in card
            assert "fortune_telling" in card
            assert "keywords" in card
            assert "meanings" in card
            assert "archetype" in card
            assert "hebrew_alphabet" in card
            assert "numerology" in card
            assert "elemental" in card
            assert "mythical_spiritual" in card
            assert "questions_to_ask" in card


def test_get_spread_data_error(test_app):
    with test_app.app_context():
        with pytest.raises(InternalServerError):
            get_spread_data(999)  # Assume 999 is an ID that doesn't exist
