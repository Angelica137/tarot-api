from app.models.spread_model import Spread
from app.models.card_model import Card
import random
from flask import abort


def get_spread(spread_id):
    spread = Spread.query.get(spread_id)
    if not spread:
        abort(404, description="Spread not found")
    return spread


def generate_random_cards(spread, number_of_cards):
    all_cards = Card.query.all()
    return random.sample(all_cards, number_of_cards)


def get_spread_data(spread_id):
    try:
        spread = get_spread(spread_id)
        selected_cards = generate_random_cards(spread, spread.number_of_cards)
        layout_description = spread.layout.layout_description
        return {
            'spread': spread.to_dict(),
            'layout_name': spread.layout.name,
            'cards': [
                {
                    'position': i + 1,
                    'description': layout_description[i],
                    'card': card.to_dict()
                } for i, card in enumerate(selected_cards)
            ]
        }
    except Exception as e:
        abort(500, description=f"Error getting spread data: {str(e)}")
