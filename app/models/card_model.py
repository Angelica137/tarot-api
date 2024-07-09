import json
from app import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    arcana = db.Column(db.String(100), nullable=False)
    suit = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(200), nullable=False)
    fortune_telling = db.Column(
        db.Text, nullable=True)  # Stored as JSON string
    keywords = db.Column(db.Text, nullable=True)  # Stored as JSON string
    meanings = db.Column(db.Text, nullable=True)  # Stored as JSON string
    archetype = db.Column(db.String(100))
    hebrew_alphabet = db.Column(db.String(50))
    numerology = db.Column(db.String(100))
    elemental = db.Column(db.String(50))
    mythical_spiritual = db.Column(db.Text)
    questions_to_ask = db.Column(db.Text)  # Stored as JSON string

    def __repr__(self):
        return '<Card {}>'.format(self.name)

    @staticmethod
    # defines a method that does not need access to instance specific data
    def from_dict(data):
        return Card(
            name=data['name'],
            number=data['number'],
            arcana=data['arcana'],
            suit=data['suit'],
            img=data['img'],
            fortune_telling=json.dumps(data['fortune_telling']),
            keywords=json.dumps(data['keywords']),
            meanings=json.dumps(data['meanings']),
            archetype=data['Archetype'],
            hebrew_alphabet=data['Hebrew Alphabet'],
            numerology=data['Numerology'],
            elemental=data['Elemental'],
            mythical_spiritual=data['Mythical/Spiritual'],
            questions_to_ask=json.dumps(data['Questions to Ask'])
        )

    def to_dict(self):
        return {
            'name': self.name,
            'number': self.number,
            'arcana': self.arcana,
            'suit': self.suit,
            'img': self.img,
            'fortune_telling': json.loads(self.fortune_telling),
            'keywords': json.loads(self.keywords),
            'meanings': json.loads(self.meanings),
            'Archetype': self.archetype,
            'Hebrew Alphabet': self.hebrew_alphabet,
            'Numerology': self.numerology,
            'Elemental': self.elemental,
            'Mythical/Spiritual': self.mythical_spiritual,
            'Questions to Ask': json.loads(self.questions_to_ask)
        }
