import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, Table
from flask import Flask, request, redirect, render_template

app = Flask(__name__, template_folder="./static/templates")
engine = create_engine("sqlite:///Models/2019.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

metadata = MetaData(bind=engine)
users = Table('predictiondata', metadata, autoload=True)

class Item(object):
    def __init__(self, name, age, defense, iso, bb, strikeout, sb, babip, prediction):
        self.name = name
        self.age = age
        self.defense = defense
        self.iso = iso
        self.bb = bb
        self.strikeout = strikeout
        self.sb = sb
        self.babip = babip
        self.prediction = prediction
            

@app.route('/')
def test():
    result = engine.execute("SELECT Name, Team, Position, Age, DEF, ISO, BB, K, SB, BABIP, Prediction FROM predictiondata WHERE Name == 'Willians Astudillo'").first()
    print("Result:", result.Name)
    return render_template("index.html", Name=result.Name, Team=result.Team, Position=result.Position, Predicted=result.Prediction, Age=result.Age, Def=result.DEF, Iso=result.ISO, BB=result.BB, Strikeout=result.K, SB=result.SB, Babip=result.BABIP )

@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        resulted = request.form
        firstName = resulted['name']
        query = "SELECT Name, Team, Position, Age, DEF, ISO, BB, K, SB, BABIP, Prediction FROM predictiondata WHERE Name == '{}'".format(firstName)
        result = engine.execute(query).first()
        return render_template("index.html", Name=result.Name, Team=result.Team, Position=result.Position, Predicted=result.Prediction, Age=result.Age, Def=result.DEF, Iso=result.ISO, BB=result.BB, Strikeout=result.K, SB=result.SB, Babip=result.BABIP )




if __name__ == '__main__':
    app.run(debug=True)
