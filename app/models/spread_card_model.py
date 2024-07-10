# -*- coding: utf-8 -*-
from app import db
from app.models.spread_model import Spread
from app.models.card_model import Card


class SpreadCard(db.Model):
    __tablename__ = "spread_card"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False)
    position_name = db.Column(db.String(256), nullable=False)
    position_interpretation = db.Column(db.String(256), nullable=False)
    spread_id = db.Column(
        db.Integer,
        db.ForeignKey('spread.id'),
        nullable=False
    )
    card_id = db.Column(
        db.Integer,
        db.ForeignKey('card.id'),
        nullable=False
    )
