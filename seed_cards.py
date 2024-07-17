import os
import json
from app import create_app, db
from app.models.card_model import Card
from sqlalchemy.exc import IntegrityError


def seed_cards():
    with open('tarot-images.json', 'r') as f:
        data = json.load(f)

    cards_data = data.get('cards', [])
    print(f"Number of cards to process: {len(cards_data)}")

    cards_to_add = []
    for card_data in cards_data:
        # Debug print statements
        for key, value in card_data.items():
            if isinstance(value, str) and len(value) > 50:
                print(f"Warning: '{key}' exceeds 50 characters. Length: {len(value)}")
                print(f"Value: {value[:100]}...")  # Print first 100 chars

        img_filename = card_data.get('img', '')
        img_path = os.path.join('app', 'static', 'images', 'cards',
                                img_filename)
        if not os.path.exists(img_path):
            print(f"Warning: Image file {img_path} not found")

        try:
            card = Card(
                name=card_data.get('name'),
                number=card_data.get('number'),
                arcana=card_data.get('arcana'),
                suit=card_data.get('suit'),
                img=card_data.get('img'),
                fortune_telling=json.dumps(
                    card_data.get('fortune_telling', [])),
                keywords=json.dumps(card_data.get('keywords', [])),
                meanings=json.dumps(card_data.get('meanings', {})),
                archetype=card_data.get('Archetype'),
                hebrew_alphabet=card_data.get('Hebrew Alphabet'),
                numerology=card_data.get('Numerology'),
                elemental=card_data.get('Elemental'),
                mythical_spiritual=card_data.get('Mythical/Spiritual'),
                questions_to_ask=json.dumps(card_data.get('Questions to Ask',
                                                          [])),
                affirmation=card_data.get('Affirmation'),
                astrology=card_data.get('Astrology')
            )
            cards_to_add.append(card)
        except Exception as e:
            print(f"Error processing card {card_data.get('name')}: {str(e)}")

    try:
        db.session.bulk_save_objects(cards_to_add)
        db.session.commit()
        print(f"Successfully added {len(cards_to_add)} cards to the database.")
    except IntegrityError:
        db.session.rollback()
        print(
            "Error: Some cards already exist in the database. No changes were made.")
    except Exception as e:
        db.session.rollback()
        print(
            f"An error occurred while adding cards to the database: {str(e)}")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_cards()
