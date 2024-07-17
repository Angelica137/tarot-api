from app import db, create_app
from sqlalchemy import text


def clear_tables():
    # Clear tables in reverse order of dependencies
    db.session.execute(text("DELETE FROM readings"))
    db.session.execute(text("DELETE FROM users"))
    db.session.execute(text("DELETE FROM spreads"))
    db.session.execute(text("DELETE FROM spread_layouts"))

    # If you have a spread_cards table, uncomment the following line
    # db.session.execute(text('DELETE FROM spread_cards'))

    db.session.commit()
    print("All tables cleared successfully!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        clear_tables()
