# -*- coding: utf-8 -*-
import json
from app import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    arcana = db.Column(db.String(200), nullable=False)
    suit = db.Column(db.String(200), nullable=False)
    img = db.Column(db.String(200), nullable=False)
    fortune_telling = db.Column(
        db.Text, nullable=True)  # Stored as JSON string
    keywords = db.Column(db.Text, nullable=True)  # Stored as JSON string
    meanings = db.Column(db.Text, nullable=True)  # Stored as JSON string
    archetype = db.Column(db.String(200))
    hebrew_alphabet = db.Column(db.String(200))
    numerology = db.Column(db.String(200))
    elemental = db.Column(db.String(200))
    mythical_spiritual = db.Column(db.Text)
    astrology = db.Column(db.String(200))
    affirmation = db.Column(db.String(200))
    questions_to_ask = db.Column(db.Text)  # Stored as JSON string

    def __repr__(self):
        return '<Card {}>'.format(self.name)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            number=data['number'],
            arcana=data['arcana'],
            suit=data['suit'],
            img=data['img'],
            fortune_telling=json.dumps(data['fortune_telling']),
            keywords=json.dumps(data['keywords']),
            meanings=json.dumps(data['meanings']),
            archetype=data['archetype'],
            hebrew_alphabet=data['hebrew_alphabet'],
            numerology=data['numerology'],
            elemental=data['elemental'],
            mythical_spiritual=data['mythical_spiritual'],
            questions_to_ask=json.dumps(data['questions_to_ask']),
            affirmation=data.get('affirmation'),
            astrology=data.get('astrology')
        )

    def to_dict(self):
        return {
            "id": self.id,
            'name': self.name,
            'number': self.number,
            'arcana': self.arcana,
            'suit': self.suit,
            'img': self.img,
            'fortune_telling': json.loads(self.fortune_telling),
            'keywords': json.loads(self.keywords),
            'meanings': json.loads(self.meanings),
            'archetype': self.archetype,
            'hebrew_alphabet': self.hebrew_alphabet,
            'numerology': self.numerology,
            'elemental': self.elemental,
            'mythical_spiritual': self.mythical_spiritual,
            'questions_to_ask': json.loads(self.questions_to_ask),
            'affirmation': self.affirmation,
            'astrology': self.astrology
        }