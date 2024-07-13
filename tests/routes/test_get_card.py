import pytest
import json
from app import create_app, db
from app.models.card_model import Card


def test_get_existing_card(client):
    with client.application.app_context():
        # Prepare the test data
        card_data = {
            "name": "The Fool",
            "number": "0",
            "arcana": "Major Arcana",
            "suit": "Trump",
            "img": "m00.jpg",
            "fortune_telling": json.dumps(["Watch for new projects and new beginnings"]),
            "keywords": json.dumps(["freedom"]),
            "meanings": json.dumps({"light": [
                "Freeing yourself from limitation"]}),
            "archetype": "The Divine Madman",
            "hebrew_alphabet": "Aleph/Ox/1",
            "numerology": "0 (off the scale; pure potential)",
            "elemental": "Air",
            "mythical_spiritual": "Adam before the fall...",
            "questions_to_ask": json.dumps(["What would I do if I felt free to take a leap?"]),
            "affirmation": "I am open to all possibilities.",
            "astrology": "Uranus, Air"
        }

        # Create and add the test card
        test_card = Card(**card_data)
        db.session.add(test_card)
        db.session.commit()

        added_card = Card.query.filter_by(name="The Fool").first()
        assert added_card is not None, "Card was not added to the database"

        response = client.get(f'/api/card/{added_card.id}')
        print(f"Response: {response.data}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.get_json()
        assert data is not None, "Response data is None"
        assert data['name'] == 'The Fool'
        assert data['img'] == 'm00.jpg'
        assert data['number'] == '0'
        assert data['arcana'] == 'Major Arcana'
        assert data['suit'] == 'Trump'
        assert data['fortune_telling'] == [
            "Watch for new projects and new beginnings"]
        assert data['keywords'] == ["freedom"]
        assert data['meanings'] == {
            "light": ["Freeing yourself from limitation"]}
        assert data['questions_to_ask'] == [
            "What would I do if I felt free to take a leap?"]


def test_get_non_existing_card(client):
    response = client.get('/api/card/9999')
    print(f"Response: {response.data}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.get_json()
    assert data is not None, "Response data should not be None"
    assert 'error' in data
    assert 'not found' in data['error'].lower()
