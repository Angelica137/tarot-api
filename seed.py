import os
import json
from app import create_app, db
from app.models.card_model import Card
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout


def seed_cards():
    with open('tarot-images.json', 'r') as f:
        data = json.load(f)

    # print(f"Type of data: {type(data)}")
    # print(f"Keys in data: {data.keys()}")

    cards_data = data.get('cards', [])
    print(f"Number of cards: {len(cards_data)}")

    for card_data in cards_data:
        # Debug print statements
        for key, value in card_data.items():
            if isinstance(value, str) and len(value) > 50:
                print(f"Warning: '{key}' exceeds 50 characters. Length: {len(value)}")
                print(f"Value: {value[:100]}...")  # Print first 100 chars

        img_filename = card_data.get('img', '')
        img_path = os.path.join('app', 'static', 'images', 'cards', img_filename)
        if not os.path.exists(img_path):
            print(f"Warning: Image file {img_path} not found")

        card = Card(
            name=card_data.get('name'),
            number=card_data.get('number'),
            arcana=card_data.get('arcana'),
            suit=card_data.get('suit'),
            img=card_data.get('img'),
            fortune_telling=json.dumps(card_data.get('fortune_telling', [])),
            keywords=json.dumps(card_data.get('keywords', [])),
            meanings=json.dumps(card_data.get('meanings', {})),
            archetype=card_data.get('Archetype'),
            hebrew_alphabet=card_data.get('Hebrew Alphabet'),
            numerology=card_data.get('Numerology'),
            elemental=card_data.get('Elemental'),
            mythical_spiritual=card_data.get('Mythical/Spiritual'),
            questions_to_ask=json.dumps(card_data.get('Questions to Ask', [])),
            affirmation=card_data.get('Affirmation'),
            astrology=card_data.get('Astrology')
        )

        db.session.add(card)


def seed_spreads_and_layouts():
    # Three card spread
    three_card_layout = SpreadLayout(
        name='Three Card Spread',
        layout_description=json.dumps({
            "type": "three_card_spread",
            "positions": [
                {"x": 0, "y": 0},
                {"x": 150, "y": 0},
                {"x": 300, "y": 0}
            ]
        })
    )
    db.session.add(three_card_layout)

    # Celtic Cross
    celtic_cross_layout = SpreadLayout(
        name='Celtic Cross',
        layout_description=json.dumps({
            "type": "celtic_cross",
            "positions": [
                {"x": 100, "y": 100},  # Center
                {"x": 150, "y": 100},  # Crossing
                {"x": 100, "y": 0},    # Above
                {"x": 100, "y": 200},  # Below
                {"x": 0, "y": 100},    # Past
                {"x": 200, "y": 100},  # Future
                {"x": 300, "y": 0},    # Self
                {"x": 300, "y": 75},   # Environment
                {"x": 300, "y": 150},  # Hopes/Fears
                {"x": 300, "y": 225}   # Outcome
            ]
        })
    )
    db.session.add(celtic_cross_layout)
    db.session.flush()

    three_card_spread = Spread(
        name='Past, Present, Future',
        number_of_cards=3,
        layout_id=three_card_layout.id  # I think this is meant to be called by id
    )
    db.session.add(three_card_spread)

    celtic_cross_spread = Spread(
        name='Celtic Cross',
        number_of_cards=10,
        layout_id=celtic_cross_layout.id
    )
    db.session.add(celtic_cross_spread)


def seed_all():
    seed_spreads_and_layouts()
    seed_cards()
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_all()
