# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from app.auth.auth import requires_auth
from app.services.spread_service import get_spread_data
from app.models.spread_model import Spread
from app.models.card_model import Card
from app.models.spread_layout_model import SpreadLayout
import random
import json


spread_api_bp = Blueprint('spread', __name__)


@spread_api_bp.route('/spread/<int:spread_id>', methods=['GET', 'POST'])
def get_spread(spread_id):
    if request.method == 'GET':
        return jsonify(get_spread_data(spread_id)), 200

    elif request.method == 'POST':
        data = request.json
        question = data.get('question')
        spread_data = get_spread_data(spread_id)
        spread_data['question'] = question if question else None
        return jsonify(spread_data), 200
