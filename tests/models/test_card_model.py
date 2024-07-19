import pytest
from app.models.card_model import Card
import json


@pytest.fixture
def sample_card_data():
    return {
        "name": "The Fool",
        "number": "0",
        "arcana": "Major Arcana",
        "suit": "Trump",
        "img": "m00.jpg",
        "fortune_telling": ["Watch for new projects and new beginnings"],
        "keywords": ["freedom"],
        "meanings": {"light": ["Freeing yourself from limitation"]},
        "archetype": "The Divine Madman",
        "hebrew_alphabet": "Aleph/Ox/1",
        "numerology": "0 (off the scale; pure potential)",
        "elemental": "Air",
        "mythical_spiritual": "Adam before the fall...",
        "questions_to_ask": ["What would I do if I felt free to take a leap?"],
        "affirmation": "I am open to all possibilities.",
        "astrology": "Uranus, Air",
    }


def test_new_card(test_app, sample_card_data):
    """
    GIVEN a Card model
    WHEN a new Card is created
    THEN check the name, description, id, created_at, and updated_at fields
    """
    new_card = Card.from_dict(sample_card_data)
    assert new_card.name == "The Fool"
    assert new_card.number == "0"
    assert new_card.arcana == "Major Arcana"
    assert new_card.suit == "Trump"
    assert new_card.img == "m00.jpg"
    assert (
        json.loads(new_card.fortune_telling)[0]
        == "Watch for new projects and new beginnings"
    )
    assert json.loads(new_card.keywords)[0] == "freedom"
    assert (
        json.loads(new_card.meanings)["light"][0] == "Freeing yourself from limitation"
    )
    assert new_card.archetype == "The Divine Madman"
    assert new_card.hebrew_alphabet == "Aleph/Ox/1"
    assert new_card.numerology == "0 (off the scale; pure potential)"
    assert new_card.elemental == "Air"
    assert "Adam before the fall" in new_card.mythical_spiritual
    assert (
        json.loads(new_card.questions_to_ask)[0]
        == "What would I do if I felt free to take a leap?"
    )
    assert new_card.affirmation == "I am open to all possibilities."
    assert new_card.astrology == "Uranus, Air"


def test_card_representation(sample_card_data):
    """
    GIVEN a Card instance
    WHEN __repr__() is called
    THEN it should return a string with teh card's name
    """
    card = Card.from_dict(sample_card_data)
    assert repr(card) == "<Card The Fool>"


def test_card_to_dict(sample_card_data):
    """
    GIVEN a Card instance
    WHEN to_dict() is called
    THEN it should return a dictionary with the card's data
    """
    card = Card.from_dict(sample_card_data)  # Change to use from_dict
    card_dict = card.to_dict()
    for key, value in sample_card_data.items():
        if isinstance(value, list):
            assert card_dict[key] == json.loads(json.dumps(value))
        else:
            assert card_dict[key] == value
    assert "id" in card_dict


def test_card_from_dict(sample_card_data):
    """
    GIVEN a Card model
    WHEN a new Card is created from a dictionary
    THEN check the card is created correctly
    """
    new_card = Card.from_dict(sample_card_data)
    assert isinstance(new_card, Card)
