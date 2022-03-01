"""Seed file to make sample data for db."""

from models import User_Info, db, Feedback
from app import app

# (venv) python seed.py

#Create tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
User_Info.query.delete()

#Create Pets
taco = User_Info(username = 'taco', password = 'taco', email = 'taco@gamil.com', first_name = 'Taco', last_name = 'Taco')
coffee = User_Info(username = 'coffee', password = 'coffee', email = 'coffee@gamil.com', first_name = 'Coffee', last_name = 'Coffee')

#create Feedback
f1 = Feedback(title = "Test1", content = "Test1", username_id = "taco")

# Add new pet objects to the session
db.session.add(taco)
db.session.add(coffee)

# Commit 
db.session.commit()

#add and commit feedback
db.session.add(f1)
db.session.commit()