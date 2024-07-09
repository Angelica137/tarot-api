# -*- coding: utf-8 -*-
import pytest
from app.models.spread_model import Spread
import json


def test_spread_model():
    spread_model = SpreadModel()
    assert spread_model is not None
