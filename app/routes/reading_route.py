from flask import Blueprint, jsonify, request
#from app.auth.auth import requires_premium
from app.services.spread_service import get_spread_data
from app.models.reading_model import Reading
from app import db
from datetime import datetime  # Import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging

reading_api_bp = Blueprint('reading', __name__)


@reading_api_bp.route('/readings', methods=['POST'])
#@requires_premium
def save_reading():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    print(f"Received data: {data}")
    print(f"Current user ID: {current_user_id}")

    if not data or 'question' not in data or 'spread_data' not in data:
        print(f"Missing required data. Data received: {data}")
        return jsonify({'error': 'Missing request data'}), 400

    new_reading = Reading(
        question=data['question'],
        user_id=current_user_id,
        spread_data=data['spread_data']
    )

    try:
        db.session.add(new_reading)
        db.session.commit()
    except SQLAlchemyError as e:
        logging.error(f'Error saving reading: {str(e)}')
        db.session.rollback()
        return jsonify({'error': f'Error saving reading: {str(e)}'}), 500

    return jsonify(
        {"message": "Reading saved successfully", "reading_id": new_reading.id}
    ), 201


@reading_api_bp.route('/readings/', methods=['GET'])
#@requires_premium
def get_readings():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        readings = Reading.query.filter_by(user_id=current_user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
    except SQLAlchemyError as e:
        logging.error(f'Error retrieving readings: {str(e)}')
        return jsonify({'error': f'Error retrieving readings: {str(e)}'}), 500

    return jsonify({
        'readings': [reading.to_dict() for reading in readings.items],
        'total': readings.total,
        'pages': readings.pages,
        'current_page': page,
        'has_next': readings.has_next,
        'has_prev': readings.has_prev,
    }), 200


@reading_api_bp.route('/readings/<int:reading_id>', methods=['GET', 'DELETE'])
#@requires_premium
def get_reading(reading_id):
    #urrent_user_id = get_jwt_identity()
    reading = Reading.query.filter_by(id=reading_id, user_id=current_user_id).first()

    if not reading:
        return jsonify({'error': 'Reading not found'}), 404

    if request.method == 'GET':
        return jsonify(reading.to_dict()), 200

    if request.method == 'DELETE':
        current_user_id = get_jwt_identity()
        reading = Reading.query.filter_by(id=reading_id, user_id=current_user_id).first()

        print(f"Attempting to delete reading {reading_id} for user {current_user_id}")

        if not reading:
            print(f"Reading {reading_id} not found for user {current_user_id}")
            return jsonify({'error': 'Reading not found'}), 404

        try:
            db.session.delete(reading)
            db.session.commit()
            print(f"Reading {reading_id} deleted successfully")
            return jsonify({'message': 'Reading deleted successfully'}), 200
        except Exception as e:
            print(f"Error deleting reading: {str(e)}")
            db.session.rollback()
            return jsonify({'error': f'Error deleting reading: {str(e)}'}), 500
