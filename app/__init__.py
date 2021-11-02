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

logged_in_user = ""

# renders the main page
@app.route("/")
def main_page():
    if session.get(logged_in_user):
        return redirect("/dashboard")
    return render_template("main_page.html")

# create account site
@app.route("/create_account")
def create_account():
    return render_template("login_create.html", create=True)

# handles submitting of create account
@app.route("/submit_create_account", methods=['GET', 'POST'])
def submit_create_account():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            same_password = request.form.get("same_password")
            #get data from form
            c.execute("SELECT * FROM users")
            usersTable = c.fetchall()
            #fetch user table data from db file
            if username == '':
                return render_template("login_create.html", create=True, error="Your username cannot be blank")
            userTaken = False
            for user in usersTable: # check if username is in the database
                if user[0] == username:
                    userTaken = True
            if userTaken:
                return render_template("login_create.html", create=True, error="That username has already been taken")
                # if it is, return this username has been taken error
            elif password != same_password: # if it is not, check if the passwords match
                return render_template("login_create.html", create=True, error="The passwords do not match")
                # if they do not, return passwords do not match error
            elif password == '':
                return render_template("login_create.html", create=True, error="Your password cannot be blank")
            else:
                info = [username,password,""]
                addAccount = f"INSERT INTO users VALUES(?,?,?)" # if they do, add the entry to the database
                c.execute(addAccount,info) #add user data to table
                db.commit() #save changes
                return redirect("/dashboard")
    except:
        return render_template("login_create.html", create=True, error="Error!") # overall error catch

# login page
@app.route("/login")
def login():
    return render_template("login_create.html", create=False)

# handles submitting of login
@app.route("/submit_login", methods=['GET', 'POST'])
def submit_login():
    try:
        if request.method == "POST":
            user = request.form.get("username") #get data from form
            passwd = request.form.get("password")

            c.execute("SELECT * FROM users")
            usersTable = c.fetchall() #fetch user table data from db file;
            #usersTable is a list of tuples: [(user,pass,stories), (user,pass,stories)]

            for value in usersTable:
                if value[0] == user: #check if user is in the users database
                    if value[1] == passwd: #if user is, check if password is correct
                        global logged_in_user
                        logged_in_user = user
                        session[user] = passwd
                        return redirect("/dashboard") #if everything works, log the user in successfully
                    else: #user exists, but password is wrong
                        return render_template("login_create.html", create=False, error="The password is incorrect") #call error fxn; indicate passwd is incorrect
            return render_template("login_create.html", create=False, error="That user does not exist") #call error fxn; indicate username is incorrect
            #only return this after checking all the usernames & confirming it doesn't exist
    except:
        return render_template("login_create.html", create=True, error="Error!")
        #overall catch for working site
        #c.execute("SELECT password from users WHERE username=user")

#logout page
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    global logged_in_user
    if logged_in_user in session:
        session.pop(logged_in_user)
        logged_in_user = ""
    return render_template('main_page.html')

@app.route("/dashboard")
def dashboard():
    if not session.get(logged_in_user):
        # if session doesn't have the correct login info, i.e. you are not signed in
        return render_template('main_page.html')
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
