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
        print("Seeding powers...")
        powers = [
            Power(name="Super Strength", description="Grants the wielder superhuman physical strength beyond normal human limits"),
            Power(name="Flight", description="Allows the wielder to fly through the air at incredible speeds and altitudes"),
            Power(name="Super Human Senses", description="Enhances all five senses to superhuman levels of perception and awareness"),
            Power(name="Elasticity", description="Enables the wielder to stretch their body to extreme lengths and shapes"),
            Power(name="Telekinesis", description="Grants the ability to move objects with the power of the mind alone"),
            Power(name="Invisibility", description="Allows the wielder to become completely invisible to the naked eye"),
            Power(name="Time Manipulation", description="Provides the power to slow down, speed up, or stop time itself"),
            Power(name="Energy Projection", description="Enables the wielder to project various forms of energy as attacks"),
            Power(name="Shape Shifting", description="Allows the wielder to transform their physical form into any desired shape"),
            Power(name="Telepathy", description="Grants the ability to read minds and communicate through thought alone"),
            Power(name="Super Speed", description="Enables movement at velocities far exceeding normal human capabilities"),
            Power(name="Healing Factor", description="Provides rapid regeneration and recovery from injuries and damage"),
        ]
        db.session.add_all(powers)
        db.session.flush()

        print("Seeding heroes...")
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
            Hero(name="Rogue", super_name="Anna Marie"),
            Hero(name="Emma Frost", super_name="White Queen"),
            Hero(name="Jubilee", super_name="Jubilation Lee"),
            Hero(name="Psylocke", super_name="Betsy Braddock"),
            Hero(name="She-Hulk", super_name="Jennifer Walters"),
        ]
        db.session.add_all(heroes)
        db.session.flush()
        print("Creating hero-power associations...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []
        
        for hero in heroes:
            num_powers = randint(1, 4)
            selected_powers = sample(powers, num_powers)
            
            for power in selected_powers:
                existing = db.session.query(HeroPower).filter_by(
                    hero_id=hero.id, power_id=power.id
                ).first()
                
                if not existing:
                    hero_powers.append(
                        HeroPower(hero=hero, power=power, strength=rc(strengths))
                    )
        
        db.session.add_all(hero_powers)
        db.session.commit()

        print(f"Seeding complete!")
        print(f"Created {len(users)} users")
        print(f"Created {len(powers)} powers")
        print(f"Created {len(heroes)} heroes")
        print(f"Created {len(hero_powers)} hero-power associations")

if __name__ == '__main__':
    seed_database()