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

cats = mongo.db.categories
ings = mongo.db.ingredients
recs = mongo.db.recipes
units = mongo.db.units
users = mongo.db.users


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
    return render_template("pages/profile/profile.html")


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
    recipes = recs.find()
    return render_template("pages/browse_results/browse_results.html",
                           recipes=recipes)


@app.route("/cookbook")
def cookbook():
    return render_template("pages/cookbook/cookbook.html")


@app.route("/menu")
def menu():
    return render_template("pages/menu/menu.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
