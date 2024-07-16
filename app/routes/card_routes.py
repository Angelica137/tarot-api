# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, current_app, session
from app.auth.auth import requires_auth
from app.models.card_model import Card
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app import db


api = Blueprint('api', __name__)


@api.route('/')
def hello_world():
    return "Welcome, login to continue"


@api.route('/')
def home():
    return "Welcome to the home page"


@api.route('/card/<int:card_id>', methods=['GET'])
@requires_auth('get:card')
def get_card(payload, card_id):
    current_app.logger.info(u"\U0001F7E2", f"Session contents: {session}")
    current_app.logger.info(f"Payload received: {payload}")

    current_app.logger.info(f"Attempting to retrieve card with id: {card_id}")
    card = Card.query.get(card_id)
    if card is None:
        current_app.logger.warning(f"Card with id {card_id} not found")
        return jsonify({"error": f"Card with id {card_id} not found"}), 404
    current_app.logger.info(f"Card found: {card}")
    return jsonify(card.to_dict()), 200


@api.route('/test_db')
def test_db():
    try:
        cards = Card.query.all()
        return jsonify({
            "message": f"Database connection successful. Found {len(cards)} cards."
        }), 200
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database connection failed"}), 500
