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

    def __repr__(self):
        return f"<SpreadCard {self.position_interpretation} in position {self.position_name} of spread {self.spread_id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'spread_id': self.spread_id,
            'card_id': self.card_id,
            'position': self.position,
            'position_name': self.position_name,
            'position_interpretation': self.position_interpretation
        }

    @staticmethod
    def from_dict(data):
        return SpreadCard(**data)
