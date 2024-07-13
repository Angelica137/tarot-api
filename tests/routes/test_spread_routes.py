import json
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app.models.card_model import Card

def test_get_spread(client, session):
    # Create a SpreadLayout with the correct structure
    layout = SpreadLayout(
        name='Three Card Spread',
        layout_description=json.dumps({
            "type": "linear",
            "positions": [
                {"name": "Past", "x": 0, "y": 0},
                {"name": "Present", "x": 1, "y": 0},
                {"name": "Future", "x": 2, "y": 0}
            ]
        })
    )
    session.add(layout)
    session.flush()  # This assigns an ID to layout

    # Create a Spread
    spread = Spread(
        name="Past, Present, Future",
        number_of_cards=3,
        layout_id=layout.id
    )
    session.add(spread)

    # Create some Cards
    for i in range(10):  # Create more cards than needed for the spread
        card = Card(
            name=f'Test Card {i}',
            number=str(i),
            arcana='Major' if i % 2 == 0 else 'Minor',
            suit='Wands' if i % 4 == 0 else 'Cups' if i % 4 == 1 else 'Swords' if i % 4 == 2 else 'Pentacles',
            img=f'test_image_{i}.jpg',
            fortune_telling=json.dumps([f"Fortune {i}", f"Another fortune {i}"]),
            keywords=json.dumps([f"Keyword {i}", f"Another keyword {i}"]),
            meanings=json.dumps({
                "light": [f"Light meaning {i}"],
                "shadow": [f"Shadow meaning {i}"]
            }),
            archetype=f"Archetype {i}",
            hebrew_alphabet=f"Hebrew {i}",
            numerology=f"Numerology {i}",
            elemental=f"Element {i}",
            mythical_spiritual=f"Myth {i}",
            questions_to_ask=json.dumps([f"Question {i}?", f"Another question {i}?"])
        )
        session.add(card)

    session.commit()

    response = client.get(f'/api/spread/{spread.id}')
    assert response.status_code == 200
    data = response.get_json()

    assert 'spread' in data
    assert 'layout_name' in data
    assert data['layout_name'] == 'Three Card Spread'
    assert 'cards' in data
    assert len(data['cards']) == 3

    layout_descriptions = json.loads(layout.layout_description)['positions']

    for i, card_data in enumerate(data['cards']):
        assert 'position' in card_data
        assert isinstance(card_data['position'], int)
        assert card_data['position'] == i + 1
        assert 'description' in card_data
        assert isinstance(card_data['description'], str)
        assert 'card' in card_data
        card = card_data['card']
        assert 'name' in card
        assert 'number' in card
        assert 'arcana' in card
        assert 'suit' in card
        assert 'img' in card
        assert 'fortune_telling' in card
        assert 'keywords' in card
        assert 'meanings' in card
        assert 'archetype' in card
        assert 'hebrew_alphabet' in card
        assert 'numerology' in card
        assert 'elemental' in card
        assert 'mythical_spiritual' in card
        assert 'questions_to_ask' in card

    # Check that cards are randomly selected
    card_names = set(card_data['card']['name'] for card_data in data['cards'])
    assert len(card_names) == 3
