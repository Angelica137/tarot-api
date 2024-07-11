# -*- coding: utf-8 -*-
import json
from app.extensions import db


class SpreadLayout(db.Model):
    __tablename__ = "spread_layouts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    layout_description = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<SpreadLayout {self.name}>"

    @staticmethod
    def from_dict(data):
        return SpreadLayout(
            name=data['name'],
            layout_description=json.dumps(data['layout_description'])
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "layout_description": json.loads(self.layout_description)
        }
