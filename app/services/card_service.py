import random

def generate_unique_cards(all_cards, number_of_cards):
    if len(all_cards) < number_of_cards:
        raise ValueError("Not enough cards in the deck")
    return random.sample(all_cards, number_of_cards)
