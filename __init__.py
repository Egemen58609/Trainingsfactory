
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path






app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




def create_database():
    with app.app_context():
        if not path.exists('website/' + "database.db"):
            db.create_all()
            print('Created Database!')

# Call the create_database() function
create_database()