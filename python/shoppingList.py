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

# # Mongo collections - list
# cats = list(mongo.db.categories.find())
# ings = list(mongo.db.ingredients.find())
# recs = list(mongo.db.recipes.find())
# units = list(mongo.db.units.find())

# # Current user (replace with session[user])
# user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})


def getUserShoppingList():
    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_shopping_ings = user['shopping']
    user_shopping_ings_length = len(user_shopping_ings)
    user_shopping_cupboard_ings_detail = []
    user_shopping_house_ings_detail = []
    user_shopping_spicerack_ings_detail = []
    user_shopping_ings_detail = []

    # Get ings in user's shopping_ings
    if user_shopping_ings != []:
        i = 0
        while i < user_shopping_ings_length:
            user_shopping_ing = ings_db.find_one({"_id": user_shopping_ings[i]['id']})
            # Spicerack
            if (str(user_shopping_ing['cat_name']) == "615cb7b43651f6c470f9a551"):
                user_shopping_spicerack_ings_detail.append(user_shopping_ing)
                user_shopping_spicerack_ings_detail[-1]["bag"] = user_shopping_ings[i]['bag']
            # Cupboard
            elif (str(user_shopping_ing['cat_name']) == "615cb8323651f6c470f9a552"):
                user_shopping_cupboard_ings_detail.append(user_shopping_ing)
                user_shopping_cupboard_ings_detail[-1]["bag"] = user_shopping_ings[i]['bag']
            # House
            elif (str(user_shopping_ing['cat_name']) == "615cb8473651f6c470f9a553"):
                user_shopping_house_ings_detail.append(user_shopping_ing)
                user_shopping_house_ings_detail[-1]["bag"] = user_shopping_ings[i]['bag']
            i += 1

    return user_shopping_cupboard_ings_detail, user_shopping_house_ings_detail, user_shopping_spicerack_ings_detail


def updateUserShoppingList(ing_id, profile_list):
    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_shopping = user['shopping']
    user_shopping_length = len(user_shopping)
    user_shopping_ids = []

    i = 0
    while i < user_shopping_length:
        user_shopping_ids.append(str(user_shopping[i]['id']))
        i += 1

    if ing_id in user_shopping_ids:
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$pull': {profile_list: {"id": ObjectId(ing_id)}}})
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$pull': {"shopping": {"id": ObjectId(ing_id)}}})
    else:
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {profile_list: {"id": ObjectId(ing_id), "bag": True}}})
        users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {"shopping": {"id": ObjectId(ing_id), "bag": True}}})


def toggleShoppingList(ing_id):
    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_shopping = user['shopping']
    user_shopping_length = len(user_shopping)

    i = 0
    while i < user_shopping_length:
        if (ing_id == str(user_shopping[i]['id'])):
            user_shopping_toggle = not user_shopping[i]['bag']
            # Toggle bag true/false in profile_list
            users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                        {"$set" : {"shopping"+"."+str(i)+".bag" : user_shopping_toggle}})
        i += 1