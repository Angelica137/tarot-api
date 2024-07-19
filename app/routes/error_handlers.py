from flask import jsonify, current_app


def resource_not_found(e):
    current_app.logger.error(f"404 error: {str(e)}")
    return jsonify({"error": "Resource not found"}), 404


def internal_server_error(e):
    current_app.logger.error(f"500 error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500


def bad_request(e):
    current_app.logger.error(f"400 error: {str(e)}")
    return jsonify({"error": "Bad request"}), 400


def unauthorized(e):
    current_app.logger.error(f"401 error: {str(e)}")
    return jsonify({"error": "Unauthorized"}), 401


def forbidden(e):
    current_app.logger.error(f"403 error: {str(e)}")
    return jsonify({"error": "Forbidden"}), 403


def method_not_allowed(e):
    current_app.logger.error(f"405 error: {str(e)}")
    return jsonify({"error": "Method not allowed"}), 405


# Register error handlers in your application
def register_error_handlers(app):
    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(405, method_not_allowed)
