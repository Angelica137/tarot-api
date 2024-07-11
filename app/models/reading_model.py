# -*- coding: utf-8 -*-
from datetime import datetime

from app import db


class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spread_id = db.Column(
        db.Integer, db.ForeignKey('spreads.id'), nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Reading id={self.id}, question='{self.question}', spread_id={self.spread_id}, created_at='{self.created_at}', updated_at='{self.updated_at}'>"
