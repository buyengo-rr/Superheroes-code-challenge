from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    serialize_rules = ('-created_at', '-updated_at')

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return name.strip()

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        return email.lower().strip()

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    super_name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hero_powers = db.relationship('HeroPower', backref='hero', cascade="all, delete-orphan", lazy='dynamic')

    serialize_rules = ('-hero_powers.hero', '-created_at', '-updated_at')

    @validates('name', 'super_name')
    def validate_names(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError(f"{key.replace('_', ' ').title()} must be at least 2 characters long")
        return value.strip()

    def __repr__(self):
        return f'<Hero {self.id}: {self.name} ({self.super_name})>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hero_powers = db.relationship('HeroPower', backref='power', cascade="all, delete-orphan", lazy='dynamic')

    serialize_rules = ('-hero_powers.power', '-created_at', '-updated_at')

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Power name must be at least 2 characters long")
        return name.strip()

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description.strip()) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return description.strip()

    def __repr__(self):
        return f'<Power {self.id}: {self.name}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('hero_id', 'power_id', name='unique_hero_power'),
        db.Index('idx_hero_power', 'hero_id', 'power_id'),
    )

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers', '-created_at', '-updated_at')

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of {valid_strengths}")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}: Hero ID {self.hero_id}, Power ID {self.power_id}, Strength: {self.strength}>'