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

# User cupboard
user_cupboard = user['cupboard']
user_cupboard_arr = []
icupboard_max = len(user_cupboard)

# User fav
# user_fav = user['fav']
# user_fav_arr = []
# ifav_max = len(user_fav)

# User house
user_house = user['house']
user_house_arr = []
ihouse_max = len(user_house)

# User menu
# user_menu = user['menu']
# user_menu_arr = []
# imenu_max = len(user_menu)

# User shopping
# user_shopping = user['shopping']
# user_shopping_arr = []
# ishopping_max = len(user_shopping)

# User spicerack
user_spicerack = user['spicerack']
user_spicerack_arr = []
ispicerack_max = len(user_spicerack)


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
    i = 0

    # Get ings in user's cupboard
    if user_cupboard != []:
        while i < icupboard_max:
            user_cupboard_arr.append(ings_db.find_one({"_id": user_cupboard[i]['id']}))
            user_cupboard_arr[i]["bag"] = user_cupboard[i]['bag']
            i += 1
    
    # Get ings with cupboard category
    ings_cupboard = list(ings_db.find({"cat_name": ObjectId("615cb8323651f6c470f9a552")}))

    # Get spices in user's spicerack
    i = 0

    if user_spicerack != []:
        while i < ispicerack_max:
            user_spicerack_arr.append(ings_db.find_one({"_id": user_spicerack[i]['id']}))
            user_spicerack_arr[i]["bag"] = user_spicerack[i]['bag']
            i += 1
    
    # Get ings with spice category
    ings_spices = list(ings_db.find({"cat_name": ObjectId("615cb7b43651f6c470f9a551")}))
    
    # Get items in user's house
    i = 0

    if user_house != []:
        while i < ihouse_max:
            user_house_arr.append(ings_db.find_one({"_id": user_house[i]['id']}))
            user_house_arr[i]["bag"] = user_house[i]['bag']
            i += 1
    
    # Get ings with house category
    ings_house = list(ings_db.find({"cat_name": ObjectId("615cb8473651f6c470f9a553")}))

    return render_template("pages/profile/profile.html",
                           user = user,
                           user_cupboard = user_cupboard_arr,
                           user_spices = user_spicerack_arr,
                           user_house = user_house_arr,
                           ings = ings,
                           ings_cupboard = ings_cupboard,
                           ings_spices = ings_spices,
                           ings_house = ings_house)


@app.route("/add_ingredient/<select_name>", methods=["GET", "POST"])
def add_ingredient(select_name):
    if request.method == "POST":
        ings_selected_id = request.form.getlist(select_name)
        ings_selected = ings_db.find_one({"_id": ObjectId(ings_selected_id[0])})

        # Add selected ingredient to correct category (watch add/remove CI videos) --> DONE
        # Only display ingredients on ingredients list that aren't already in spicerack
        # Make better names for accordion profile forms
        # Redirect properly

        # House
        if (ings_selected['cat_name'] == ObjectId("615cb8473651f6c470f9a553")):
            print((user['house'][0]['id']))
            users_db.update_one({"_id": ObjectId("60f19bbb944f8dacbba0b104")},
                               {'$push': {"house": {"id": ObjectId(ings_selected['_id']), "bag": True}}})

        return render_template("pages/profile/profile.html",
                            user=user,
                            ingredients=ings)


@app.route("/add_recipe")
def add_recipe():
    return render_template("pages/add_recipe/add_recipe.html")


@app.route("/view_recipe")
def view_recipe():
    return render_template("pages/view_recipe/view_recipe.html")


@app.route("/browse")
def browse():
    return render_template("pages/browse/browse.html")


@app.route("/browse_results")
def browse_results():
    return render_template("pages/browse_results/browse_results.html",
                           categories=cats,
                           recipes=recs)


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
