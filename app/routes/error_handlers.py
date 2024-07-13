from flask import jsonify, current_app


def resource_not_found(e):
    current_app.logger.error(f"404 error: {str(e)}")
    return jsonify({"error": str(e)}), 404
