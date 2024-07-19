from app import db
from flask_sqlalchemy import SQLAlchemy


class Spread(db.Model):
    __tablename__ = "spreads"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    number_of_cards = db.Column(db.Integer, nullable=False)
    layout_id = db.Column(
        db.Integer, db.ForeignKey("spread_layouts.id"), nullable=False
    )
    layout = db.relationship("SpreadLayout")
    position_meanings = db.Column(db.JSON, nullable=False)

    def __init__(self, name, number_of_cards, layout, position_meanings):
        self.name = name
        self.number_of_cards = number_of_cards
        self.layout = layout
        self.position_meanings = position_meanings

    def __repr__(self):
        return f"<Spread '{self.name}' with {self.number_of_cards} cards>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number_of_cards": self.number_of_cards,
            "layout_id": self.layout_id,
            "layout": {
                "name": self.layout.name,
                "description": self.layout.layout_description,
            }
            if self.layout
            else None,
        }

    @staticmethod
    def from_dict(spread_dict):
        return Spread(**spread_dict)  # dictionary unpacking
