import pytest
import json
from app import create_app, db
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
from app.models.card_model import Card


@pytest.fixture
def client():
    return app.test_client()