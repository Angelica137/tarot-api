# -*- coding: utf-8 -*-
import pytest
from app.models.reading_model import Reading


def test_reading_model(db):
    reading = Reading(name='Reading 1')
    db.session.add(reading)
    db.session.commit()
    assert reading.id is not None
