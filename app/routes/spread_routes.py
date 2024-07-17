# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from app.auth.auth import requires_auth
from app.services.spread_service import get_spread_data
from app.models.spread_model import Spread
from app.models.card_model import Card
from app.models.spread_layout_model import SpreadLayout
from app.models.reading_model import Reading
from app import db

import random
import json


spread_api_bp = Blueprint('spread', __name__)


@spread_api_bp.route('/spread/<int:spread_id>', methods=['GET'])
@requires_auth('get:spread')
def get_spread(payload, spread_id):
    question = request.args.get('question')
    spread_data = get_spread_data(spread_id)

    if question:
        spread_data['question'] = question

    return jsonify(spread_data), 200


@spread_api_bp.route('/spread/<int:spread_id>', methods=['POST'])
@requires_auth('post:spread')
def save_reading(payload, spread_id):
    auth0_user_id = payload.get('sub')

    if not auth0_user_id:
        return jsonify({
            'message': 'User ID not found in JWT'
        }), 401

    spread_data = get_spread_data(spread_id)
    question = request.json.get('question')

    if question:
        spread_data['question'] = question

    new_reading = Reading(
        question=question,
        auth0_user_id=auth0_user_id,
        spread_data=spread_data
    )

    db.session.add(new_reading)
    db.session.commit()

    return jsonify({
        'message': 'Reading saved successfully',
        'reading_id': new_reading.id
    }), 201
