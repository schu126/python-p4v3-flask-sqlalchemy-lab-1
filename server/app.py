# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    eq = Earthquake.query.filter(Earthquake.id == id).first()

    if eq is None:
        return make_response({
           'message': f'Earthquake {id} not found.'
        }, 404)
    
    return make_response({
        'id': eq.id,
        'location': eq.location,
        'magnitude': eq.magnitude,
        'year': eq.year
    })
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    eqs = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    eq_dicts = []
    for eq in eqs:
        eq_dict = {
            'id': eq.id,
            'magnitude': eq.magnitude,
            'location': eq.location,
            'year': eq.year
        }
        eq_dicts.append(eq_dict)
    
    return make_response({
        'count': len(eqs),
        'quakes': eq_dicts
    })


if __name__ == '__main__':
    app.run(port=5555, debug=True)
