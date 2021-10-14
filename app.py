import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env
# from functions.create_vars import *


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

# User cupboard
user_cupboard = user['cupboard']
user_cupboard_detail = []
user_cupboard_ids = []
icupboard_max = len(user_cupboard)

# Get ings in user's cupboard
if user_cupboard != []:
    i = 0
    while i < icupboard_max:
        user_cupboard_detail.append(ings_db.find_one({"_id": user_cupboard[i]['id']}))
        user_cupboard_ids.append(str(user_cupboard[i]['id']))
        user_cupboard_detail[i]["bag"] = user_cupboard[i]['bag']
        i += 1

def update_add_vars_cupboard():
    global user_cupboard
    global user_cupboard_detail
    global user_cupboard_ids

    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_cupboard = user['cupboard']
    user_cupboard_detail.append(ings_db.find_one({"_id": user_cupboard[-1]['id']}))
    user_cupboard_detail[-1]["bag"] = user_cupboard[-1]['bag']
    user_cupboard_ids.append(str(user_cupboard[-1]['id']))

    return user_cupboard, user_cupboard_detail, user_cupboard_ids


# User fav

# User house
user_house = user['house']
user_house_detail = []
user_house_ids = []
ihouse_max = len(user_house)

# Get ings in user's house
if user_house != []:
    i = 0
    while i < ihouse_max:
        user_house_detail.append(ings_db.find_one({"_id": user_house[i]['id']}))
        user_house_ids.append(str(user_house[i]['id']))
        user_house_detail[i]["bag"] = user_house[i]['bag']
        i += 1

def update_add_vars_house():
    global user_house
    global user_house_detail
    global user_house_ids

    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_house = user['house']
    user_house_detail.append(ings_db.find_one({"_id": user_house[-1]['id']}))
    user_house_detail[-1]["bag"] = user_house[-1]['bag']
    user_house_ids.append(str(user_house[-1]['id']))

    return user_house, user_house_detail, user_house_ids

# User menu

# User shopping

# User spicerack
user_spicerack = user['spicerack']
user_spicerack_detail = []
user_spicerack_ids = []
ispicerack_max = len(user_spicerack)

# Get ings in user's spicerack
if user_spicerack != []:
    i = 0
    while i < ispicerack_max:
        user_spicerack_detail.append(ings_db.find_one({"_id": user_spicerack[i]['id']}))
        user_spicerack_ids.append(str(user_spicerack[i]['id']))
        user_spicerack_detail[i]["bag"] = user_spicerack[i]['bag']
        i += 1

def update_add_vars_spicerack():
    global user_spicerack
    global user_spicerack_detail
    global user_spicerack_ids

    user = users_db.find_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")})
    user_spicerack = user['spicerack']
    user_spicerack_detail.append(ings_db.find_one({"_id": user_spicerack[-1]['id']}))
    user_spicerack_detail[-1]["bag"] = user_spicerack[-1]['bag']
    user_spicerack_ids.append(str(user_spicerack[-1]['id']))

    return user_spicerack, user_spicerack_detail, user_spicerack_ids


@app.route("/")
def index():
    return render_template("pages/index/index.html")


@app.route("/login")
def login():
    return render_template("pages/login/login.html")


@app.route("/register")
def register():
    return render_template("pages/register/register.html")


@app.route("/profile")
def profile():    
    # Get ings with cupboard category
    ings_cupboard = list(ings_db.find({"cat_name": ObjectId("615cb8323651f6c470f9a552")}))

    # Get ings with spice category
    ings_spicerack = list(ings_db.find({"cat_name": ObjectId("615cb7b43651f6c470f9a551")}))

    # Get ings with house category
    ings_house = list(ings_db.find({"cat_name": ObjectId("615cb8473651f6c470f9a553")}))

    return render_template("pages/profile/profile.html",
                           user = user,
                           user_cupboard = user_cupboard_detail,
                           user_spicerack = user_spicerack_detail,
                           user_house = user_house_detail,
                           ings = ings,
                           ings_cupboard = ings_cupboard,
                           ings_spicerack = ings_spicerack,
                           ings_house = ings_house
                           )


@app.route("/profile_toggle_ingredient/<ing_id>")
def profile_toggle_ingredient(ing_id):
    print("Hello!")

    ing_id_index = user_cupboard_ids.index(ing_id)
    users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                            {"$set" : {"cupboard."+str(ing_id_index)+".bag" : True}})
    
    # global user_cupboard
    # global user_cupboard_detail
    # global user_cupboard_ids

    # print(user_cupboard)
    # print(user_cupboard_detail)
    # print(user_cupboard_ids)

    
    # user_cupboard[index]['bag'] = not user_cupboard[index]['bag']
    # user_cupboard_detail[index]['bag'] = not user_cupboard_detail[index]['bag']

    # print("After!")
    # print(user_cupboard)
    # print(user_cupboard_detail)
    # print(user_cupboard_ids)
    return redirect(url_for("profile"))


@app.route("/profile_add_ingredient", methods=["GET", "POST"])
def profile_add_ingredient():
    if request.method == "POST":        
        ings_selected_id = request.form.getlist("ingredient")[0]
        ings_selected = ings_db.find_one({"_id": ObjectId(ings_selected_id)})

        # Cupboard
        global user_cupboard
        global user_cupboard_detail
        global user_cupboard_ids

        if (ings_selected['cat_name'] == ObjectId("615cb8323651f6c470f9a552")):
            if ings_selected_id not in user_cupboard_ids:
                users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {"cupboard": {"id": ObjectId(ings_selected['_id']), "bag": True}}})
                update_add_vars_cupboard()

        # House
        global user_house
        global user_house_detail
        global user_house_ids

        if (ings_selected['cat_name'] == ObjectId("615cb8473651f6c470f9a553")):
            if ings_selected_id not in user_house_ids:
                users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {"house": {"id": ObjectId(ings_selected['_id']), "bag": True}}})
                update_add_vars_house()
        
        # Spicerack
        global user_spicerack
        global user_spicerack_detail
        global user_spicerack_ids

        if (ings_selected['cat_name'] == ObjectId("615cb7b43651f6c470f9a551")):
            if ings_selected_id not in user_spicerack_ids:
                users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                                    {'$push': {"spicerack": {"id": ObjectId(ings_selected['_id']), "bag": True}}})
                update_add_vars_spicerack()

        return redirect(url_for("profile"))


@app.route("/add_recipe")
def add_recipe():
    return render_template("pages/add_recipe/add_recipe.html")


@app.route("/view_recipe")
def view_recipe():
    return render_template("pages/view_recipe/view_recipe.html")


@app.route("/browse")
def browse():
    return render_template("pages/browse/browse.html",
                           categories=cats)


@app.route("/browse_results")
def browse_results():
    return render_template("pages/browse_results/browse_results.html",
                           categories=cats,
                           recipes=recs)


# def add_ingredient_page():


@app.route("/add_ingredient", methods=["GET", "POST"])
def add_ingredient():
    if request.method == "POST":
        cat_str = request.form.getlist("category")[0]

        ing_new = {
            "name": request.form.get("name"),
            "url":  request.form.get("name").replace(' ', '-').lower(),
            "cat_name": ObjectId(cat_str)
        }

        ings_db.insert_one(ing_new)

        return redirect(url_for("browse"))


@app.route("/cookbook")
def cookbook():
    return render_template("pages/cookbook/cookbook.html")


@app.route("/menu")
def menu():
    return render_template("pages/menu/menu.html")


@app.route("/shopping_list")
def shopping_list():
    # Need array of ingredients, quantities in shopping list
    return render_template("pages/shopping_list/shopping_list.html",
                           ingredients=ings)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)