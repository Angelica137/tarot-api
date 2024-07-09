# -*- coding: utf-8 -*-
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
        "fortune_telling": [
            "Watch for new projects and new beginnings",
            "Prepare to take something on faith",
            "Something new comes your way; go for it"
        ],
        "keywords": [
            "freedom",
            "faith",
            "inexperience",
            "innocence"
        ],
        "meanings": {
            "light": [
                "Freeing yourself from limitation",
                "Expressing joy and youthful vigor",
                "Being open-minded",
                "Taking a leap of faith"
            ],
            "shadow": [
                "Being gullible and naive",
                "Taking unnecessary risks",
                "Failing to be serious when required"
            ]
        },
        "Archetype": "The Divine Madman",
        "Hebrew Alphabet": "Aleph/Ox/1",
        "Numerology": "0 (off the scale; pure potential)",
        "Elemental": "Air",
        "Mythical/Spiritual": "Adam before the fall. Christ as a wandering holy madman.",
        "Questions to Ask": [
            "What would I do if I felt free to take a leap?",
            "How willing am I to be vulnerable and open?",
            "How might past experiences help in this new situation?"
        ]
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
    assert json.loads(new_card.fortune_telling)[
        0] == "Watch for new projects and new beginnings"
    assert json.loads(new_card.keywords)[0] == "freedom"
    assert json.loads(new_card.meanings)[
        "light"][0] == "Freeing yourself from limitation"
    assert new_card.archetype == "The Divine Madman"
    assert new_card.hebrew_alphabet == "Aleph/Ox/1"
    assert new_card.numerology == "0 (off the scale; pure potential)"
    assert new_card.elemental == "Air"
    assert "Adam before the fall" in new_card.mythical_spiritual
    assert json.loads(new_card.questions_to_ask)[
        0] == "What would I do if I felt free to take a leap?"


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
    card = Card.from_dict(sample_card_data)
    assert card.to_dict() == sample_card_data
