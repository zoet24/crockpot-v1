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

# Mongo collections - list
cats = list(mongo.db.categories.find())
ings = list(mongo.db.ingredients.find())
recs = list(mongo.db.recipes.find())
units = list(mongo.db.units.find())

# Current user (replace with session[user])
user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})


def sortList(profile_list):
    # sortedKeys = sorted(profile_list.keys("name"), key=lambda x:x.lower())

    profile_sort = (sorted(profile_list[0], key=lambda x: x[1]))

    print(profile_list)
    print(profile_sort)