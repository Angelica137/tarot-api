# -*- coding: utf-8 -*-
import json
from app import db


class SpreadLayout(db.Model):
    __tablename__ = "spread_layouts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    layout_description = db.Column(db.JSON, nullable=False)
