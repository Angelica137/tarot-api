from flask import Blueprint, jsonify, request
from app.services.spread_service import get_spread_data
from app.models.card_model import Card
import random

reading_api_bp = Blueprint('reading', __name__)


@reading_api_bp.route('/readings', methods=['POST'])
def create_reading():
    data = request.json
    spread_id = data.get('spread_id')
    question = data.get('question')  # Optional

    if not spread_id:
        return jsonify({'error': 'Spread ID is required'}), 400

    try:
        spread_data = get_spread_data(spread_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

    all_cards = Card.query.all()

    if len(all_cards) < spread_data['number_of_cards']:
        return jsonify({'error': 'Not enough cards in the deck'}), 400

    selected_cards = random.sample(all_cards, spread_data['number_of_cards'])

    # Create a reading response without storing in the database
    reading_response = {
        'spread': spread_data,
        'question': question,
        'cards': [
            {
                'id': card.id,
                'name': card.name,
                'arcana': card.arcana,
                'suit': card.suit,
                'img': card.img,
                'fortune_telling': card.fortune_telling,
                'keywords': card.keywords,
                'meanings': card.meanings,
                'archetype': card.archetype,
                'hebrew_alphabet': card.hebrew_alphabet,
                'numerology': card.numerology,
                'elemental': card.elemental,
                'mythical_spiritual': card.mythical_spiritual,
                'questions_to_ask': card.questions_to_ask,
                'affirmation': card.affirmation,
                'astrology': card.astrology,
                'position': index + 1
            } for index, card in enumerate(selected_cards)
        ]
    }

    return jsonify(reading_response), 200
