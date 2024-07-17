from flask import Blueprint, jsonify, request
from app.auth.auth import requires_auth
from app.services.spread_service import get_spread_data
from app.models.reading_model import Reading
from app import db
from datetime import datetime  # Import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy.orm import load_only

reading_api_bp = Blueprint("reading", __name__)


@reading_api_bp.route("/readings/", methods=["GET"])
@requires_auth("get:readings")
def get_readings(payload):
    auth0_user_id = payload.get("sub")

    if not auth0_user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = max(1, min(100, int(request.args.get("per_page", 10))))
    except ValueError:
        return jsonify({"error": "Invalid page or per_page value"}), 400

    try:
        readings = Reading.query.filter_by(auth0_user_id=auth0_user_id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        if not readings.items:
            return jsonify({"error": "No readings found"}), 404

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

    except SQLAlchemyError as e:
        logging.error(f"Error retrieving readings: {str(e)}")
        return jsonify({"error": f"Error retrieving readings: {str(e)}"}), 500


@reading_api_bp.route("/readings/<int:id>", methods=["GET"])
@requires_auth("get:reading-detail")
def get_reading(payload, id):
    current_user_id = payload.get("sub")

    reading = Reading.query.get(id)
    if not reading:
        return jsonify({"error": "Reading not found"}), 404

    if reading.auth0_user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(reading.to_dict()), 200


@reading_api_bp.route("/readings/<int:reading_id>/question", methods=["PATCH"])
@requires_auth("patch:question")
def update_reading_question(payload, reading_id):
    auth0_user_id = payload.get("sub")
    
    if not auth0_user_id:
        return jsonify({"error": "User ID not found in token"}), 401

    try:
        # Query the reading without load_only
        reading = Reading.query.filter_by(id=reading_id, auth0_user_id=auth0_user_id).first()
        
        if not reading:
            return jsonify({"error": "Reading not found or you don't have permission to update it"}), 404

        # Get new question from request
        new_question = request.json.get("question")

        if new_question is None:
            return jsonify({"error": "New question not provided in request body"}), 400

        # Log the current state
        logging.info(f"Current question: {reading.question}")

        # Store old question for comparison
        old_question = reading.question

        # Update the question
        reading.question = new_question

        # Log the update attempt
        logging.info(f"Attempting to update question from '{old_question}' to '{new_question}'")

        # Commit the changes
        db.session.commit()

        # Refresh the reading object to ensure we have the latest data
        db.session.refresh(reading)

        # Verify the update
        updated_question = reading.question

        # Log the final state
        logging.info(f"Final question after update: {updated_question}")

        return jsonify({
            "message": "Reading question updated successfully" if updated_question == new_question else "Update may have failed",
            "reading_id": reading.id,
            "old_question": old_question,
            "new_question": updated_question,
            "request_question": new_question
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error updating reading question: {str(e)}")
        return jsonify({"error": "An error occurred while updating the reading question"}), 500


@reading_api_bp.route("/readings/<int:reading_id>", methods=["DELETE"])
@requires_auth("delete:reading")
def delete_reading(payload, reading_id):
    current_user_id = payload.get("sub")

    try:
        reading = Reading.query.get(reading_id)
        if not reading:
            return jsonify({"error": "Reading not found"}), 404

        if reading.auth0_user_id != current_user_id:
            return jsonify({"error": "Unauthorized to delete this reading"}), 403

        # Store reading details before deletion for the response
        reading_details = reading.to_dict()

        # Delete the reading
        db.session.delete(reading)
        db.session.commit()

        return jsonify({
            "message": "Reading successfully deleted",
            "deleted_reading": reading_details
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error deleting reading: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the reading"}), 500
