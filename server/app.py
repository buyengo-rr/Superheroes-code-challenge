from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
import logging
from functools import wraps

from models import db, Hero, Power, HeroPower, StrengthLevel, create_hero, create_power, assign_power_to_hero

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///superheroes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

CORS(app)
mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"errors": ["Database integrity error"]}), 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"errors": ["An unexpected error occurred"]}), 500
    return decorated_function

def validate_json_data(required_fields=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"errors": ["Request must be JSON"]}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({"errors": ["No data provided"]}), 400
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({"errors": [f"Missing required fields: {', '.join(missing_fields)}"]}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }), 200

@app.route('/api/heroes', methods=['GET'])
@handle_errors
def get_heroes():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search = request.args.get('search', '')
    
    query = Hero.query
    if search:
        query = query.filter(
            Hero.name.ilike(f'%{search}%') | 
            Hero.super_name.ilike(f'%{search}%')
        )
    
    heroes = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        "heroes": [hero.to_dict(include_powers=False) for hero in heroes.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": heroes.total,
            "pages": heroes.pages,
            "has_next": heroes.has_next,
            "has_prev": heroes.has_prev
        }
    }), 200

@app.route('/api/heroes', methods=['POST'])
@handle_errors
@validate_json_data(required_fields=['name', 'super_name'])
def create_hero_endpoint():
    data = request.get_json()
    
    hero = create_hero(
        name=data['name'],
        super_name=data['super_name']
    )
    
    db.session.commit()
    return jsonify(hero.to_dict()), 201

@app.route('/api/heroes/<int:id>', methods=['GET'])
@handle_errors
def get_hero(id):
    hero = Hero.query.get_or_404(id)
    return jsonify(hero.to_dict(include_powers=True)), 200

@app.route('/api/heroes/<int:id>', methods=['PATCH'])
@handle_errors
@validate_json_data()
def update_hero(id):
    hero = Hero.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        hero.name = data['name']
    if 'super_name' in data:
        hero.super_name = data['super_name']
    
    db.session.commit()
    return jsonify(hero.to_dict()), 200

@app.route('/api/heroes/<int:id>', methods=['DELETE'])
@handle_errors
def delete_hero(id):
    hero = Hero.query.get_or_404(id)
    db.session.delete(hero)
    db.session.commit()
    return jsonify({"message": "Hero deleted successfully"}), 200

@app.route('/api/powers', methods=['GET'])
@handle_errors
def get_powers():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search = request.args.get('search', '')
    
    query = Power.query
    if search:
        query = query.filter(
            Power.name.ilike(f'%{search}%') | 
            Power.description.ilike(f'%{search}%')
        )
    
    powers = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        "powers": [power.to_dict(include_heroes=False) for power in powers.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": powers.total,
            "pages": powers.pages,
            "has_next": powers.has_next,
            "has_prev": powers.has_prev
        }
    }), 200

@app.route('/api/powers', methods=['POST'])
@handle_errors
@validate_json_data(required_fields=['name', 'description'])
def create_power_endpoint():
    data = request.get_json()
    
    power = create_power(
        name=data['name'],
        description=data['description']
    )
    
    db.session.commit()
    return jsonify(power.to_dict()), 201

@app.route('/api/powers/<int:id>', methods=['GET'])
@handle_errors
def get_power(id):
    power = Power.query.get_or_404(id)
    include_heroes = request.args.get('include_heroes', 'false').lower() == 'true'
    return jsonify(power.to_dict(include_heroes=include_heroes)), 200

@app.route('/api/powers/<int:id>', methods=['PATCH'])
@handle_errors
@validate_json_data()
def update_power(id):
    power = Power.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        power.name = data['name']
    if 'description' in data:
        power.description = data['description']
    
    db.session.commit()
    return jsonify(power.to_dict()), 200

@app.route('/api/powers/<int:id>', methods=['DELETE'])
@handle_errors
def delete_power(id):
    power = Power.query.get_or_404(id)
    db.session.delete(power)
    db.session.commit()
    return jsonify({"message": "Power deleted successfully"}), 200

@app.route('/api/hero_powers', methods=['GET'])
@handle_errors
def get_hero_powers():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    hero_id = request.args.get('hero_id', type=int)
    power_id = request.args.get('power_id', type=int)
    
    query = HeroPower.query
    if hero_id:
        query = query.filter(HeroPower.hero_id == hero_id)
    if power_id:
        query = query.filter(HeroPower.power_id == power_id)
    
    hero_powers = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        "hero_powers": [hp.to_dict() for hp in hero_powers.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": hero_powers.total,
            "pages": hero_powers.pages,
            "has_next": hero_powers.has_next,
            "has_prev": hero_powers.has_prev
        }
    }), 200

@app.route('/api/hero_powers', methods=['POST'])
@handle_errors
@validate_json_data(required_fields=['strength', 'power_id', 'hero_id'])
def create_hero_power():
    data = request.get_json()
    
    hero_power = assign_power_to_hero(
        hero_id=data['hero_id'],
        power_id=data['power_id'],
        strength_level=data['strength']
    )
    
    db.session.commit()
    return jsonify(hero_power.to_dict()), 201

@app.route('/api/hero_powers/<int:id>', methods=['PATCH'])
@handle_errors
@validate_json_data()
def update_hero_power(id):
    hero_power = HeroPower.query.get_or_404(id)
    data = request.get_json()
    
    if 'strength' in data:
        hero_power.strength = data['strength']
    
    db.session.commit()
    return jsonify(hero_power.to_dict()), 200

@app.route('/api/hero_powers/<int:id>', methods=['DELETE'])
@handle_errors
def delete_hero_power(id):
    hero_power = HeroPower.query.get_or_404(id)
    db.session.delete(hero_power)
    db.session.commit()
    return jsonify({"message": "Hero power deleted successfully"}), 200

@app.route('/api/strength_levels', methods=['GET'])
def get_strength_levels():
    return jsonify({
        "strength_levels": [level.value for level in StrengthLevel]
    }), 200

@app.route('/api/send_mail', methods=['POST'])
@handle_errors
@validate_json_data(required_fields=['to', 'subject', 'body'])
def send_mail():
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        return jsonify({"errors": ["Mail configuration not set up"]}), 400
    
    data = request.get_json()
    
    msg = Message(
        subject=data['subject'],
        sender=app.config['MAIL_DEFAULT_SENDER'] or app.config['MAIL_USERNAME'],
        recipients=[data['to']],
        body=data['body']
    )
    
    if 'html' in data:
        msg.html = data['html']
    
    mail.send(msg)
    logger.info(f"Email sent to {data['to']}")
    return jsonify({"message": "Email sent successfully"}), 200

@app.route('/api/stats', methods=['GET'])
@handle_errors
def get_stats():
    total_heroes = Hero.query.count()
    total_powers = Power.query.count()
    total_hero_powers = HeroPower.query.count()
    
    strength_distribution = db.session.query(
        HeroPower.strength,
        db.func.count(HeroPower.id)
    ).group_by(HeroPower.strength).all()
    
    return jsonify({
        "total_heroes": total_heroes,
        "total_powers": total_powers,
        "total_hero_powers": total_hero_powers,
        "strength_distribution": {
            str(strength): count for strength, count in strength_distribution
        }
    }), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)