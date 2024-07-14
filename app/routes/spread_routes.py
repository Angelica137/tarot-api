# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app
from app.models.spread_model import Spread
from app.models.card_model import Card
from app.models.spread_layout_model import SpreadLayout
import random
import json


spread_api_bp = Blueprint('spread', __name__)


@spread_api_bp.route('/spread/<int:spread_id>', methods=['GET'])
def get_spread(spread_id):
    spread = Spread.query.get_or_404(spread_id)
    all_cards = Card.query.all()

    selected_cards = random.sample(all_cards, spread.number_of_cards)

    layout_description = spread.layout.layout_description

    result = {
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

    return jsonify(result), 200
