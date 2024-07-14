from app.models.spread_model import Spread
from flask import abort


def get_spread(spread_id):
    spread = Spread.query.get(spread_id)
    if not spread:
        abort(404, description="Spread not found")
    return spread


def get_spread_data(spread_id):
    try:
        spread = get_spread(spread_id)
        return spread.to_dict()
    except Exception as e:
        abort(500, description=f"Error getting spread data: {str(e)}")
