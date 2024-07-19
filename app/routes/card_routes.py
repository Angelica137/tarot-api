from flask import Blueprint, jsonify, request, current_app, session
from app.auth.auth import requires_auth
from app.models.card_model import Card
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app import db


api = Blueprint("api", __name__)


@api.route("/")
def api_info():
    return jsonify(
        {
            "name": "Tarot API",
            "version": "1.0",
            "description": "API for tarot card information",
        }
    )


@api.route("/cards/<int:card_id>", methods=["GET"])
@requires_auth("get:card")
def get_card(payload, card_id):
    current_app.logger.info("\U0001F7E2", f"Session contents: {session}")
    current_app.logger.info(f"Payload received: {payload}")

    current_app.logger.info(f"Attempting to retrieve card with id: {card_id}")
    card = Card.query.get(card_id)
    if card is None:
        current_app.logger.warning(f"Card with id {card_id} not found")
        return jsonify({"error": f"Card with id {card_id} not found"}), 404
    current_app.logger.info(f"Card found: {card}")
    return jsonify(card.to_dict()), 200


@api.route("/api/debug/db-test")
def db_test():
    try:
        # Try to query the database
        card_count = Card.query.count()
        return jsonify({"status": "success", "card_count": card_count})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
