from app import db, create_app
from app.models.user_model import User
from app.models.reading_model import Reading
from app.models.spread_model import Spread
from app.models.spread_layout_model import SpreadLayout
import json


def seed_database():
    # Three card layout
    three_card_layout_linear = SpreadLayout(
        name='Three Card Spread',
        layout_description=json.dumps({
            "type": "three_card_linear",
            "positions": [
                {"name": 1, "x": 0, "y": 0},
                {"name": 2, "x": 150, "y": 0},
                {"name": 3, "x": 300, "y": 0}
            ]
        })
    )
    db.session.add(three_card_layout_linear)

    # Celtic Cross
    celtic_cross_layout = SpreadLayout(
        name='Celtic Cross',
        layout_description=json.dumps({
            "type": "celtic_cross",
            "positions": [
                {"name": 1, "x": 100, "y": 100},
                {"name": 2, "x": 150, "y": 100},
                {"name": 3, "x": 100, "y": 0},
                {"name": 4, "x": 100, "y": 200},
                {"name": 5, "x": 0, "y": 100},
                {"name": 6, "x": 200, "y": 100},
                {"name": 7, "x": 300, "y": 0},
                {"name": 8, "x": 300, "y": 75},
                {"name": 9, "x": 300, "y": 150},
                {"name": 10, "x": 300, "y": 225}
            ]
        })
    )
    db.session.add(celtic_cross_layout)

    # Three card spread
    past_present_future_spread = Spread(
        name="Past, Present, Future",
        number_of_cards=3,
        layout=three_card_layout_linear,
        position_meanings={
            1: "Past",
            2: "Present",
            3: "Future"
        }
    )
    db.session.add(past_present_future_spread)

    three_card_spread_situation = Spread(
        name="Situation, Action, Outcome",
        number_of_cards=3,
        layout=three_card_layout_linear,
        position_meanings={
            1: "Situation",
            2: "Action",
            3: "Outcome"
        }
    )
    db.session.add(three_card_spread_situation)

    # Celtic Cross spread
    celtic_cross_spread = Spread(
        name="Celtic Cross",
        number_of_cards=10,
        layout=celtic_cross_layout,
        position_meanings={
            1: "Present",
            2: "Challenge",
            3: "Basis",
            4: "Past",
            5: "Crown",
            6: "Future",
            7: "Self",
            8: "Environment",
            9: "Hopes/Fears",
            10: "Outcome"
        }
    )
    db.session.add(celtic_cross_spread)

    # Create test user premium
    user = User(
        auth0_user_id="auth0|669538ee4b1a2e5770dbad9f",
        email="premium_user@oracle.com",
        name="Premium User",
        role="premium"
    )

    db.session.add(user)
    db.session.commit()

    # Create three readings for the user
    readings = [
        Reading(
            question="What's my career outlook?",
            user_id=user.id,
            spread_data={
                "spread_id": past_present_future_spread.id,
                "cards": [
                    {
                        "position": "Past",
                        "card_id": 1,
                        "name": "The Fool",
                        "meaning": "New beginnings"
                    },
                    {
                        "position": "Present",
                        "card_id": 10,
                        "name": "Wheel of Fortune",
                        "meaning": "Change"
                    },
                    {
                        "position": "Future",
                        "card_id": 21,
                        "name": "The World",
                        "meaning": "Completion"
                    }
                ]
            }
        ),
        Reading(
            question="How's my love life?",
            user_id=user.id,
            spread_data={
                "spread_id": past_present_future_spread.id,
                "cards": [
                    {
                        "position": "Past",
                        "card_id": 6,
                        "name": "The Lovers",
                        "meaning": "Harmony"
                    },
                    {
                        "position": "Present",
                        "card_id": 13,
                        "name": "Death",
                        "meaning": "Transformation"
                    },
                    {
                        "position": "Future",
                        "card_id": 19,
                        "name": "The Sun",
                        "meaning": "Joy"
                    }
                ]
            }
        ),
        Reading(
            question="What should I focus on this month?",
            user_id=user.id,
            spread_data={
                "spread_id": past_present_future_spread.id,
                "cards": [
                    {
                        "position": "Past",
                        "card_id": 4,
                        "name": "The Emperor",
                        "meaning": "Authority"
                    },
                    {
                        "position": "Present",
                        "card_id": 11,
                        "name": "Justice",
                        "meaning": "Fairness"
                    },
                    {
                        "position": "Future",
                        "card_id": 14,
                        "name": "Temperance",
                        "meaning": "Balance"
                    }
                ]
            }
        )
    ]

    for reading in readings:
        db.session.add(reading)

    db.session.commit()
    print("Database seeded successfully!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()
