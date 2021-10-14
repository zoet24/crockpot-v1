import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Mongo collections
cats_db = mongo.db.categories
ings_db = mongo.db.ingredients
recs_db = mongo.db.recipes
units_db = mongo.db.units
users_db = mongo.db.users


# def create_vars_house():
#     user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
#     user_house = user['house'] # List of ingredients objIds and bool if they are/aren't in bag
#     user_house_detail = [] # Expanded list of ingredients objIds and details, and bool if they are/aren't in bag
#     user_house_ids = [] # List of ingredients IDs in house for quick search
#     ihouse_max = len(user_house) # Number of ingredients in house

#     # Get ings in user's house
#     if user_house != []:
#         i = 0
#         while i < ihouse_max:
#             user_house_detail.append(ings_db.find_one({"_id": user_house[i]['id']}))
#             user_house_detail[i]["bag"] = user_house[i]['bag']
#             user_house_ids.append(str(user_house[i]['id']))
#             i += 1

#     return user_house_detail, user_house_ids

def update_vars_house():
    global user_house
    global user_house_detail
    global user_house_ids

    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_house = user['house']
    # user_house_detail.append(ings_db.find_one({"_id": user_house[-1]['id']}))
    # user_house_detail[-1]["bag"] = user_house[-1]['bag']
    user_house_ids.append(str(user_house[-1]['id']))
    
    print("Update:")
    print(user_house)
    print(user_house_detail)
    print(user_house_ids)

    return user_house, user_house_detail, user_house_ids