# Team fourCoffeePeanuts: Ryan Wang (PM), Eliza Knapp, Yaying Liang Li, Jesse Xie
# SoftDev
# P00 -- Move Slowly and Fix Things

# setup
from flask import Flask, render_template, request, redirect, session # flask imports
import sqlite3   #enable control of an sqlite database

app = Flask(__name__) #creates flask object

# TODO: configure session stuff
app.secret_key = "random" # TODO: perhaps change to urandom(32)

DB_FILE="walnutLatte.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

create = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, stories TEXT) " # create users table
c.execute((create))
create = "CREATE TABLE IF NOT EXISTS stories (name TEXT, latestUpdate TEXT, fullStory TEXT) " # create stories table
c.execute((create))

# renders the main page
@app.route("/")
def main_page():
    print("dasda")
    return render_template("main_page.html")

# create account site
@app.route("/create_account")
def create_account():
    return render_template("login_create.html", create=True)

# handles submitting of create account
@app.route("/submit_create_account", methods=['GET', 'POST'])
def submit_create_account():
    # try
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
            
        info = [username,password,"da"]
        addAccount = f"INSERT INTO users VALUES(?,?,?)"
        c.execute(addAccount,info)
        db.commit() #save changes
        return render_template("main_page.html")
        # check if username is in the database
            # if it is, return this username has been taken error
            # if it is not, check if the passwords match
                # if they do, add the entry to the database
                # if they do not, return passwords do not match error
    # overall catch here to make sure site never breaks

# login site
@app.route("/login")
def login():
    return render_template("login_create.html", create=False)

# handles submitting of login
'''
@app.route("/submit_login")
def submit_login():
    # try
    if request.method == "POST":
        # check if username is in database
            # if it is, check password
                # if everything works, log the user in successfully
                # if the password is wrong, return that error
            # if the username is not, return username wrong error
    # overall catch for working site
'''


if __name__ == "__main__":
    app.debug = True
    app.run()
