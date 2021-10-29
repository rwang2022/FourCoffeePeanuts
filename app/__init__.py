#Team fourCoffeePeanuts: Ryan Wang (PM), Eliza Knapp, Yaying Liang Li, Jesse Xie
#SoftDev
#P00 -- Move Slowly and Fix Things

from flask import Flask, render_template #Q0: What happens if you remove render_template from this line?
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "No hablo queso!"
