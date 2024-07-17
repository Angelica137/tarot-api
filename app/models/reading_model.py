# -*- coding: utf-8 -*-
from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSON


class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    auth0_user_id = db.Column(
        db.String(64), db.ForeignKey('users.auth0_user_id'), nullable=False)
    spread_data = db.Column(JSON, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = db.relationship('User', back_populates='readings')

    def __init__(self, question, auth0_user_id, spread_data):
        self.question = question
        self.auth0_user_id = auth0_user_id
        self.spread_data = spread_data

    def __repr__(self):
        return (f"<Reading id={self.id}, question='{self.question[:20]}...', "
                f"spread_data={self.spread_data}, "
                f"created_at='{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}', "
                f"updated_at='{self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}'>"
                )

    @staticmethod
    def from_dict(data):
        return Reading(**data)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'auth0_user_id': self.auth0_user_id,
            'spread_data': self.spread_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
