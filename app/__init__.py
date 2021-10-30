# Team fourCoffeePeanuts: Ryan Wang (PM), Eliza Knapp, Yaying Liang Li, Jesse Xie
# SoftDev
# P00 -- Move Slowly and Fix Things

# setup 
from flask import Flask, render_template, request, redirect, session # flask imports
from flask_session import Session # creates a session instance
app = Flask(__name__) #creates flask object

app.secret_key = "random" # TODO: perhaps change to urandom(32)

@app.route("/")
def main_page():
    return render_template("mainPage.html")

if __name__ == "__main__":
    app.debug = True
    app.run()