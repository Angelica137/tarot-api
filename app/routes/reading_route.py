from flask import Blueprint, jsonify, request
from app.auth.auth import requires_auth
from app.services.spread_service import get_spread_data
from app.models.reading_model import Reading
from app import db
from datetime import datetime  # Import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging

reading_api_bp = Blueprint("reading", __name__)


@reading_api_bp.route("/reading/<int:id>", methods=["GET"])
@requires_auth("get:reading")
def get_reading(payload, id):
    current_user_id = payload.get("sub")

    reading = Reading.query.get(id)
    if not reading:
        return jsonify({"error": "Reading not found"}), 404

    if reading.auth0_user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(reading.to_dict()), 200


@reading_api_bp.route("/readings/", methods=["GET"])
def get_readings():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    try:
        readings = Reading.query.filter_by(user_id=current_user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving readings: {str(e)}")
        return jsonify({"error": f"Error retrieving readings: {str(e)}"}), 500

    return (
        jsonify(
            {
                "readings": [reading.to_dict() for reading in readings.items],
                "total": readings.total,
                "pages": readings.pages,
                "current_page": page,
                "has_next": readings.has_next,
                "has_prev": readings.has_prev,
            }
        ),
        200,
    )
