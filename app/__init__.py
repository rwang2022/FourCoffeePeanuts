# Team fourCoffeePeanuts: Ryan Wang (PM), Eliza Knapp, Yaying Liang Li, Jesse Xie
# SoftDev
# P00 -- Move Slowly and Fix Things

# setup 
from flask import Flask, render_template, request, redirect, session # flask imports
from flask_session import Session # creates a session instance
app = Flask(__name__) #creates flask object

# TODO: configure session stuff
app.secret_key = "random" # TODO: perhaps change to urandom(32)

# renders the main page
@app.route("/")
def main_page():
    return render_template("main_page.html")

# create account site
@app.route("/create_account")
def create_account():
    return render_template("login_create.html", create=True)

# login site
@app.route("/login")
def login():
    return render_template("login_create.html", create=False)

if __name__ == "__main__":
    app.debug = True
    app.run()