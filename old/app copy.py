import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env
from python.profile import getUserProfileIngs, updateUserProfileIngs, toggleUserProfileIngs
from python.shoppingList import getUserShoppingList, updateUserShoppingList, toggleShoppingList
from python.utility import sortList

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
    # Get list of ings in user's cupboard
    user_cupboard = getUserProfileIngs('cupboard')
    # Get list of ings in user's house
    user_house = getUserProfileIngs('house')
    # Get list of ings in user's spicerack
    user_spicerack = getUserProfileIngs('spicerack')

    # Get list of ings with cupboard category
    ings_cupboard = list(ings_db.find({"cat_name": ObjectId("615cb8323651f6c470f9a552")}))
    # Get list of ings with house category
    ings_house = list(ings_db.find({"cat_name": ObjectId("615cb8473651f6c470f9a553")}))
    # Get list of ings with spice category
    ings_spicerack = list(ings_db.find({"cat_name": ObjectId("615cb7b43651f6c470f9a551")}))
    
    return render_template("pages/profile/profile.html",
                           user = user,
                           user_cupboard = user_cupboard,
                           user_house = user_house,
                           user_spicerack = user_spicerack,
                           ings_cupboard = ings_cupboard,
                           ings_house = ings_house,
                           ings_spicerack = ings_spicerack,
                           )


@app.route("/profile_update_ing/<profile_list>", methods=["GET", "POST"])
def profile_update_ing(profile_list):
    if request.method == "POST":
        ing_id = request.form.getlist("ingredient")[0]
        updateUserProfileIngs(ing_id, profile_list)

    return redirect(url_for("profile"))


@app.route("/profile_toggle_ing/<ing_id>/<profile_list>")
def profile_toggle_ing(ing_id, profile_list):
    toggleUserProfileIngs(ing_id, profile_list)

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
    shopping_ings = getUserShoppingList()
    shopping_cupboard_ings = shopping_ings[0]
    shopping_house_ings = shopping_ings[1]
    shopping_spicerack_ings = shopping_ings[2]

    # Get list of ings with cupboard category
    ings_cupboard = list(ings_db.find({"cat_name": ObjectId("615cb8323651f6c470f9a552")}))
    # Get list of ings with house category
    ings_house = list(ings_db.find({"cat_name": ObjectId("615cb8473651f6c470f9a553")}))
    # Get list of ings with spice category
    ings_spicerack = list(ings_db.find({"cat_name": ObjectId("615cb7b43651f6c470f9a551")}))

    sortList(ings_spicerack)
    
    # Need array of ingredients, quantities in shopping list
    return render_template("pages/shopping_list/shopping_list.html",
                            shopping_cupboard_ings = shopping_cupboard_ings,
                            shopping_house_ings = shopping_house_ings,
                            shopping_spicerack_ings = shopping_spicerack_ings,
                            ings_cupboard = ings_cupboard,
                            ings_house = ings_house,
                            ings_spicerack = ings_spicerack,)


@app.route("/shopping_update_list/<profile_list>", methods=["GET", "POST"])
def shopping_update_list(profile_list):
    if request.method == "POST":
        ing_id = request.form.getlist("ingredient")[0]
        updateUserShoppingList(ing_id, profile_list)

    return redirect(url_for("shopping_list"))


@app.route("/shopping_list_toggle_ing/<ing_id>")
def shopping_list_toggle_ing(ing_id):
    toggleShoppingList(ing_id)

    return redirect(url_for("shopping_list"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)