# -*- coding: utf-8 -*-
import pytest
from app.models.spread_card_model import SpreadCard
import json


@pytest.fixture
def sample_spread_card_data():
    return {
        "id": 1,
        "position": 1,
        "interpretation": "Sample interpretation",
        "spread_id": 1,
        "card_id": 1
    }


def test_new_spread_card(sample_spread_card_data):
    """
    GIVEN a SpreadCard model
    WHEN a new SpreadCard is created
    THEN check the id, position, interpretation, spread_id, and card_id are correct
    """
    new_spread_card = SpreadCard(**sample_spread_card_data)
    assert new_spread_card.id == 1
    assert new_spread_card.position == 1
    assert new_spread_card.interpretation == "Sample interpretation"
    assert new_spread_card.spread_id == 1
    assert new_spread_card.card_id == 1

