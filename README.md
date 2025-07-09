# Superheroes Flask API

## Description
A Flask RESTful API to manage superheroes and their powers. Tracks heroes, powers, and the strength of each hero's powers.

## Features
- Track heroes and their super names
- Track powers and their descriptions
- Assign strengths for each hero-power connection
- Validation for strength and description
- Full REST API (GET, PATCH, POST)
- Error handling and proper status codes
- Email sending capability via Flask-Mail

## Setup
1. Clone repo and `cd` into it
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Edit email config in `app.py`
5. `flask db upgrade`
6. `python seed.py`
7. `flask run`

## Endpoints
- `GET /heroes`
- `GET /heroes/<id>`
- `GET /powers`
- `GET /powers/<id>`
- `PATCH /powers/<id>`
- `POST /hero_powers`
- `POST /send_mail`

## Contact
Owner: [Your Name]

## License
MIT
