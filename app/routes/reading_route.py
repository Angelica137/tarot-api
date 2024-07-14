from flask import Blueprint, jsonify, request, current_app
from app.models.spread_model import Spread
from app.models.card_model import Card
from app.models.reading_model import Reading
from app import db
import random


reading_api_bp = Blueprint('reading', __name__)


@reading_api_bp.route('/reading', methods=['POST'])
def create_reading():
    data = request.json
    spread_id = data.get('spread_id')
    question = data.get('question')

    if not spread_id:
        return jsonify({'error': 'Spread ID is required'}), 400

    spread = Spread.query.get_or_404(spread_id)
    all_cards = Card.query.all()

    if len(all_cards) < spread.number_of_cards:
        return jsonify({'error': 'Not enough cards in the deck'}), 400

    selected_cards = random.sample(all_cards, spread.number_of_cards)

    reading = Reading(spread_id=spread_id, question=question, cards=selected_cards)
    db.session.add(reading)
    db.session.flush()

    return jsonify(reading.to_dict()), 201
