from flask import Blueprint, jsonify, current_app
from app.models.card_model import Card

utility_bp = Blueprint('utility', __name__)


@utility_bp.route('/test_db')
def test_db():
    try:
        cards = Card.query.all()
        return jsonify({
            "message": f"Database connection successful. Found {len(cards)} cards."
        }), 200
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database connection failed"}), 500
