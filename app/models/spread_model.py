# -*- coding: utf-8 -*-
import json
from app import db


class Spread(db.Model):
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
