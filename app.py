from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

# add an api endpoint to flask app
@app.route('/api/data')
def get_data():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "John",
        "LastName": "Mortensen",
        "DOB": "October 21",
        "Residence": "San Diego",
        "Email": "jmortensen@powayusd.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Shane",
        "LastName": "Lopez",
        "DOB": "February 27",
        "Residence": "San Diego",
        "Email": "slopez@powayusd.com",
        "Owns_Cars": ["2021-Insight"]
    })
    
    return jsonify(InfoDb)

# add an HTML endpoint to flask app
@app.route('/')
def say_hello():
    html_content = """
    <html>
    <head>
        <title>Hellox</title>
    </head>
    <body>
        <h2>Hello, World!</h2>
    </body>
    </html>
    """
    return html_content

@app.route('/api/affirmation')
def get():
    affirmations = [
        # General Self-Worth
        "I am enough just as I am.",
        "I deserve love and respect.",
        "I choose to focus on my strengths.",
        "I am proud of the progress I’ve made.",
        "I trust myself to make the right decisions.",
        
        # Confidence and Empowerment
        "I am capable of achieving great things.",
        "I radiate confidence and positivity.",
        "Challenges are opportunities for growth.",
        "I am in charge of my own destiny.",
        "My potential is limitless.",
        
        # Health and Well-Being
        "I am strong and healthy.",
        "My body deserves care and nourishment.",
        "I honor my need for rest and rejuvenation.",
        "Every breath I take fills me with calm.",
        "I am grateful for my body and its abilities.",
        
        # Love and Relationships
        "I attract love and positivity.",
        "I communicate with honesty and kindness.",
        "I deserve meaningful connections.",
        "I am surrounded by supportive and loving people.",
        "I give and receive love freely."
    ]
    
    return jsonify(random.choice(affirmations))


if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)