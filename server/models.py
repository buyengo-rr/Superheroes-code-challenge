from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint
from datetime import datetime
import enum

db = SQLAlchemy()


class StrengthLevel(enum.Enum):
    """Enum for strength levels to ensure type safety"""
    WEAK = "Weak"
    AVERAGE = "Average"
    STRONG = "Strong"


class Hero(db.Model):
    __tablename__ = 'heroes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<Hero {self.name} ({self.super_name})>'
    
    @validates('name', 'super_name')
    def validate_strings(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value.strip()
    
    def to_dict(self, include_powers=True):
        result = {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_powers:
            result["hero_powers"] = [hp.to_dict(include_hero=False) for hp in self.hero_powers]
        
        return result
    
    def add_power(self, power, strength_level):
        """Add a power to this hero with specified strength level"""
        if isinstance(strength_level, str):
            strength_level = StrengthLevel(strength_level)
        
        # Check if hero already has this power
        existing = HeroPower.query.filter_by(hero_id=self.id, power_id=power.id).first()
        if existing:
            existing.strength = strength_level.value
            return existing
        
        hero_power = HeroPower(hero=self, power=power, strength=strength_level.value)
        db.session.add(hero_power)
        return hero_power
    
    def remove_power(self, power):
        """Remove a power from this hero"""
        hero_power = HeroPower.query.filter_by(hero_id=self.id, power_id=power.id).first()
        if hero_power:
            db.session.delete(hero_power)
            return True
        return False
    
    def get_powers(self):
        """Get all powers for this hero"""
        return [hp.power for hp in self.hero_powers]


class Power(db.Model):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<Power {self.name}>'
    
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Power name cannot be empty")
        return value.strip()
    
    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value.strip()
    
    def to_dict(self, include_heroes=False):
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_heroes:
            result["heroes"] = [
                {
                    "id": hp.hero.id,
                    "name": hp.hero.name,
                    "super_name": hp.hero.super_name,
                    "strength": hp.strength
                }
                for hp in self.hero_powers
            ]
        
        return result
    
    def get_heroes(self):
        """Get all heroes who have this power"""
        return [hp.hero for hp in self.hero_powers]


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Enum(StrengthLevel), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ensure a hero can't have the same power twice
    __table_args__ = (UniqueConstraint('hero_id', 'power_id', name='unique_hero_power'),)
    
    def __repr__(self):
        return f'<HeroPower {self.hero.name if self.hero else "Unknown"} - {self.power.name if self.power else "Unknown"} ({self.strength.value if isinstance(self.strength, StrengthLevel) else self.strength})>'
    
    @validates('strength')
    def validate_strength(self, key, value):
        if isinstance(value, StrengthLevel):
            return value
        
        if isinstance(value, str):
            try:
                return StrengthLevel(value)
            except ValueError:
                pass
        
        valid_values = [level.value for level in StrengthLevel]
        raise ValueError(f"Strength must be one of: {', '.join(valid_values)}")
    
    def to_dict(self, include_hero=True, include_power=True):
        result = {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength.value if isinstance(self.strength, StrengthLevel) else self.strength,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_power and self.power:
            result["power"] = self.power.to_dict(include_heroes=False)
        
        if include_hero and self.hero:
            result["hero"] = {
                "id": self.hero.id,
                "name": self.hero.name,
                "super_name": self.hero.super_name
            }
        
        return result


# Utility functions for common operations
def create_hero(name, super_name):
    """Create a new hero"""
    hero = Hero(name=name, super_name=super_name)
    db.session.add(hero)
    return hero


def create_power(name, description):
    """Create a new power"""
    power = Power(name=name, description=description)
    db.session.add(power)
    return power


def assign_power_to_hero(hero_id, power_id, strength_level):
    """Assign a power to a hero with specified strength"""
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    
    if not hero:
        raise ValueError(f"Hero with id {hero_id} not found")
    if not power:
        raise ValueError(f"Power with id {power_id} not found")
    
    return hero.add_power(power, strength_level)


def get_hero_with_powers(hero_id):
    """Get hero with all their powers"""
    hero = Hero.query.get(hero_id)
    if not hero:
        return None
    return hero.to_dict(include_powers=True)


def get_power_with_heroes(power_id):
    """Get power with all heroes who have it"""
    power = Power.query.get(power_id)
    if not power:
        return None
    return power.to_dict(include_heroes=True)