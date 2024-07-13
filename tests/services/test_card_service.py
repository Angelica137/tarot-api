import random
from app.services.card_service import generate_unique_cards
from app.models.card_model import Card


def test_generate_unique_cards():
    all_cards = [Card(id=i, name=f'Card {i}') for i in range(1, 10)]
    number_of_cards = 5
    result = generate_unique_cards(all_cards, number_of_cards)
    assert len(result) == number_of_cards
    assert len(set(result)) == len(result)
