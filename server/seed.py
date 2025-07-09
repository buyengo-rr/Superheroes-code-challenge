import os
import sys
import random
from datetime import datetime

from models import db, Hero, Power, HeroPower, StrengthLevel, create_hero, create_power, assign_power_to_hero
from app import app

def clear_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

def seed_heroes():
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"},
        {"name": "Natasha Romanoff", "super_name": "Black Widow"},
        {"name": "Diana Prince", "super_name": "Wonder Woman"},
        {"name": "Kara Zor-El", "super_name": "Supergirl"},
        {"name": "Barbara Gordon", "super_name": "Batgirl"},
        {"name": "Selina Kyle", "super_name": "Catwoman"},
        {"name": "Raven Darkholme", "super_name": "Mystique"},
        {"name": "Anna Marie", "super_name": "Rogue"},
        {"name": "Emma Frost", "super_name": "White Queen"},
        {"name": "Jessica Drew", "super_name": "Spider-Woman"},
        {"name": "Jennifer Walters", "super_name": "She-Hulk"}
    ]
    
    heroes = []
    for hero_data in heroes_data:
        try:
            hero = create_hero(hero_data["name"], hero_data["super_name"])
            heroes.append(hero)
        except Exception as e:
            print(f"Error creating hero {hero_data['name']}: {e}")
    
    return heroes

def seed_powers():
    powers_data = [
        {
            "name": "Super Strength",
            "description": "Grants the wielder superhuman physical strength, allowing them to lift massive objects and overpower opponents with ease."
        },
        {
            "name": "Flight",
            "description": "Provides the ability to fly through the air at incredible speeds, defying gravity and soaring through the skies effortlessly."
        },
        {
            "name": "Super Human Senses",
            "description": "Enhances all five senses to superhuman levels, allowing detection of the smallest sounds, scents, and movements from great distances."
        },
        {
            "name": "Elasticity",
            "description": "Allows the user to stretch their body to extreme lengths and shapes, making them nearly impossible to contain or harm through physical means."
        },
        {
            "name": "Telepathy",
            "description": "Grants the ability to read minds, communicate telepathically, and manipulate thoughts of others across vast distances."
        },
        {
            "name": "Energy Projection",
            "description": "Enables the user to generate and project various forms of energy, including plasma blasts, force fields, and destructive beams."
        },
        {
            "name": "Invisibility",
            "description": "Allows the user to become completely invisible to the naked eye and most detection methods, perfect for stealth operations."
        },
        {
            "name": "Time Manipulation",
            "description": "Provides control over the flow of time, allowing the user to slow down, speed up, or even stop time in localized areas."
        },
        {
            "name": "Weather Control",
            "description": "Grants dominion over all weather patterns, including the ability to summon storms, lightning, tornadoes, and other meteorological phenomena."
        },
        {
            "name": "Shapeshifting",
            "description": "Allows the user to alter their physical form at will, taking on the appearance of other people, animals, or objects."
        },
        {
            "name": "Teleportation",
            "description": "Enables instant transportation from one location to another, bypassing physical barriers and covering vast distances in seconds."
        },
        {
            "name": "Regeneration",
            "description": "Provides accelerated healing abilities, allowing the user to recover from injuries rapidly and potentially regrow lost limbs."
        },
        {
            "name": "Technopathy",
            "description": "Grants the ability to communicate with and control electronic devices and computer systems through mental interface."
        },
        {
            "name": "Phasing",
            "description": "Allows the user to alter their molecular density, enabling them to pass through solid objects and become intangible at will."
        },
        {
            "name": "Precognition",
            "description": "Provides glimpses of future events, allowing the user to anticipate dangers and make strategic decisions based on forthcoming possibilities."
        }
    ]
    
    powers = []
    for power_data in powers_data:
        try:
            power = create_power(power_data["name"], power_data["description"])
            powers.append(power)
        except Exception as e:
            print(f"Error creating power {power_data['name']}: {e}")
    
    return powers

def seed_hero_powers(heroes, powers):
    strength_levels = [level.value for level in StrengthLevel]
    hero_power_assignments = [
        {"hero_name": "Ms. Marvel", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "Ms. Marvel", "power_name": "Elasticity", "strength": "Strong"},
        {"hero_name": "Ms. Marvel", "power_name": "Shapeshifting", "strength": "Average"},
        
        {"hero_name": "Spider-Gwen", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "Spider-Gwen", "power_name": "Super Human Senses", "strength": "Strong"},
        {"hero_name": "Spider-Gwen", "power_name": "Precognition", "strength": "Average"},
        
        {"hero_name": "The Wasp", "power_name": "Flight", "strength": "Strong"},
        {"hero_name": "The Wasp", "power_name": "Phasing", "strength": "Average"},
        
        {"hero_name": "Scarlet Witch", "power_name": "Energy Projection", "strength": "Strong"},
        {"hero_name": "Scarlet Witch", "power_name": "Telepathy", "strength": "Strong"},
        {"hero_name": "Scarlet Witch", "power_name": "Time Manipulation", "strength": "Average"},
        
        {"hero_name": "Captain Marvel", "power_name": "Flight", "strength": "Strong"},
        {"hero_name": "Captain Marvel", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "Captain Marvel", "power_name": "Energy Projection", "strength": "Strong"},
        
        {"hero_name": "Dark Phoenix", "power_name": "Telepathy", "strength": "Strong"},
        {"hero_name": "Dark Phoenix", "power_name": "Energy Projection", "strength": "Strong"},
        {"hero_name": "Dark Phoenix", "power_name": "Teleportation", "strength": "Strong"},
        
        {"hero_name": "Storm", "power_name": "Weather Control", "strength": "Strong"},
        {"hero_name": "Storm", "power_name": "Flight", "strength": "Strong"},
        
        {"hero_name": "Shadowcat", "power_name": "Phasing", "strength": "Strong"},
        {"hero_name": "Shadowcat", "power_name": "Technopathy", "strength": "Average"},
        
        {"hero_name": "Black Widow", "power_name": "Super Human Senses", "strength": "Average"},
        {"hero_name": "Black Widow", "power_name": "Regeneration", "strength": "Weak"},
        
        {"hero_name": "Wonder Woman", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "Wonder Woman", "power_name": "Flight", "strength": "Strong"},
        {"hero_name": "Wonder Woman", "power_name": "Precognition", "strength": "Average"},
        
        {"hero_name": "Supergirl", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "Supergirl", "power_name": "Flight", "strength": "Strong"},
        {"hero_name": "Supergirl", "power_name": "Super Human Senses", "strength": "Strong"},
        
        {"hero_name": "Mystique", "power_name": "Shapeshifting", "strength": "Strong"},
        {"hero_name": "Mystique", "power_name": "Regeneration", "strength": "Average"},
        
        {"hero_name": "Rogue", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "Rogue", "power_name": "Flight", "strength": "Average"},
        
        {"hero_name": "White Queen", "power_name": "Telepathy", "strength": "Strong"},
        {"hero_name": "White Queen", "power_name": "Shapeshifting", "strength": "Average"},
        
        {"hero_name": "Spider-Woman", "power_name": "Super Strength", "strength": "Average"},
        {"hero_name": "Spider-Woman", "power_name": "Flight", "strength": "Average"},
        {"hero_name": "Spider-Woman", "power_name": "Super Human Senses", "strength": "Strong"},
        
        {"hero_name": "She-Hulk", "power_name": "Super Strength", "strength": "Strong"},
        {"hero_name": "She-Hulk", "power_name": "Regeneration", "strength": "Strong"},
    ]
    
    hero_dict = {hero.super_name: hero for hero in heroes}
    power_dict = {power.name: power for power in powers}
    
    hero_powers = []
    for assignment in hero_power_assignments:
        try:
            hero = hero_dict.get(assignment["hero_name"])
            power = power_dict.get(assignment["power_name"])
            
            if hero and power:
                hero_power = assign_power_to_hero(
                    hero.id, 
                    power.id, 
                    assignment["strength"]
                )
                hero_powers.append(hero_power)
        except Exception as e:
            print(f"Error assigning power {assignment['power_name']} to {assignment['hero_name']}: {e}")
    
    remaining_heroes = [h for h in heroes if h.super_name not in [a["hero_name"] for a in hero_power_assignments]]
    for hero in remaining_heroes:
        num_powers = random.randint(1, 3)
        available_powers = random.sample(powers, min(num_powers, len(powers)))
        
        for power in available_powers:
            try:
                strength = random.choice(strength_levels)
                hero_power = assign_power_to_hero(hero.id, power.id, strength)
                hero_powers.append(hero_power)
            except Exception as e:
                print(f"Error randomly assigning power {power.name} to {hero.super_name}: {e}")
    
    return hero_powers

def print_seeding_summary(heroes, powers, hero_powers):
    print("\n" + "="*60)
    print("SEEDING SUMMARY")
    print("="*60)
    print(f"Heroes created: {len(heroes)}")
    print(f"Powers created: {len(powers)}")
    print(f"Hero-Power relationships: {len(hero_powers)}")
    print(f"Database seeded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\nHeroes:")
    for hero in heroes[:10]:
        power_count = len([hp for hp in hero_powers if hp.hero_id == hero.id])
        print(f"  - {hero.name} ({hero.super_name}) - {power_count} powers")
    
    if len(heroes) > 10:
        print(f"  ... and {len(heroes) - 10} more heroes")
    
    print("\nPowers:")
    for power in powers[:10]:
        hero_count = len([hp for hp in hero_powers if hp.power_id == power.id])
        print(f"  - {power.name} - {hero_count} heroes")
    
    if len(powers) > 10:
        print(f"  ... and {len(powers) - 10} more powers")

def main():
    try:
        print("Starting database seeding...")
        
        with app.app_context():
            clear_database()
            print("Database cleared and recreated.")
            
            heroes = seed_heroes()
            print(f"Seeded {len(heroes)} heroes.")
            
            powers = seed_powers()
            print(f"Seeded {len(powers)} powers.")
            
            db.session.commit()
            print("Heroes and powers committed to database.")
            
            hero_powers = seed_hero_powers(heroes, powers)
            print(f"Created {len(hero_powers)} hero-power relationships.")
            
            db.session.commit()
            print("Hero-power relationships committed to database.")
            
            print_seeding_summary(heroes, powers, hero_powers)
            
    except Exception as e:
        print(f"Error during seeding: {e}")
        if 'db' in locals():
            db.session.rollback()
        sys.exit(1)

if __name__ == "__main__":
    main()