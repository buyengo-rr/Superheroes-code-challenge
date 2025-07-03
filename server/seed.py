from random import choice as rc, randint, sample
from app import app
from models import db, Hero, Power, HeroPower, User

def seed_database():
    with app.app_context():
        print("Clearing database...")
        db.session.query(HeroPower).delete()
        db.session.query(Hero).delete()
        db.session.query(Power).delete()
        db.session.query(User).delete()
        db.session.commit()

        print("Seeding users...")
        users = [
            User(name="Peter Parker", email="peter@dailybugle.com"),
            User(name="Mary Jane Watson", email="mj@broadway.com"),
            User(name="Tony Stark", email="tony@starkindustries.com"),
            User(name="Pepper Potts", email="pepper@starkindustries.com"),
            User(name="Bruce Banner", email="bruce@avengers.org"),
            User(name="Natasha Romanoff", email="natasha@shield.gov"),
            User(name="Steve Rogers", email="steve@avengers.org"),
            User(name="Thor Odinson", email="thor@asgard.com"),
        ]
        db.session.add_all(users)
        db.session.flush()