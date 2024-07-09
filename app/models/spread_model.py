# -*- coding: utf-8 -*-
import json
from app import db


class Spread(db.Model):
    __tablename__ = "spreads"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    number_of_cards = db.Column(db.Integer, nullable=False)
    layout_id = db.Column(
        db.Integer,
        db.ForeignKey('layout.id'),
        nullable=False
    )

    def __repr__(self):
        return f"<Spread '{self.name}' with {self.number_of_cards} cards>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number_of_cards": self.number_of_cards,
            "layout_id": self.layout_id
        }

    @staticmethod
    def from_dict(spread_dict):
        return Spread(**spread_dict)  # dictionary unpacking