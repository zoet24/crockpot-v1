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


# Choices for profile_list - cupboard, house, spicerack
def getUserProfileIngs(profile_list):
    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_profile_ings = user[profile_list]
    user_profile_ings_length = len(user_profile_ings)
    user_profile_ings_detail = []

    # Get ings in user's profile_ings
    if user_profile_ings != []:
        i = 0
        while i < user_profile_ings_length:
            user_profile_ings_detail.append(ings_db.find_one({"_id": user_profile_ings[i]['id']}))
            user_profile_ings_detail[i]["bag"] = user_profile_ings[i]['bag']
            i += 1

    return user_profile_ings_detail


def updateUserProfileIngs(ing_id, profile_list):
    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_profile_ings = user[profile_list]
    user_profile_ings_length = len(user_profile_ings)
    user_profile_ings_ids = []

    i = 0
    while i < user_profile_ings_length:
        user_profile_ings_ids.append(str(user_profile_ings[i]['id']))
        i += 1

    if ing_id in user_profile_ings_ids:
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$pull': {profile_list: {"id": ObjectId(ing_id)}}})
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$pull': {"shopping": {"id": ObjectId(ing_id)}}})
    else:
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {profile_list: {"id": ObjectId(ing_id), "bag": True}}})
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {"shopping": {"id": ObjectId(ing_id), "bag": True}}})


def toggleUserProfileIngs(ing_id, profile_list):
    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_profile_ings = user[profile_list]
    user_profile_ings_length = len(user_profile_ings)

    i = 0
    while i < user_profile_ings_length:
        if (ing_id == str(user_profile_ings[i]['id'])):
            user_profile_ings_toggle = not user_profile_ings[i]['bag']
            # Toggle bag true/false in profile_list
            users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                        {"$set" : {str(profile_list)+"."+str(i)+".bag" : user_profile_ings_toggle}})
            # Push/pull ingredient from shopping list
            if (user_profile_ings_toggle == True):
                users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {"shopping": {"id": ObjectId(ing_id), "bag": True}}})
            else:
                users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$pull': {"shopping": {"id": ObjectId(ing_id)}}})
        i += 1