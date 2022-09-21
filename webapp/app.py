
from flask import Flask , render_template,request,url_for,redirect,flash
import pymongo 
from pymongo import MongoClient



client = pymongo.MongoClient("mongodb+srv://aryan:abc1234@clients.k7mgg9r.mongodb.net/?retryWrites=true&w=majority")
db = client["clients"]
details=db["details"]
 
app = Flask(__name__)

app.secret_key = 'abc'

@app.route("/",methods=["POST","GET"])
def data():

    if request.method=="POST":
        print("POST")
        username=request.form["username"]
        password=request.form["password"]
        print(username,password)
        if details.count_documents({"username":username}):
            flash('Username already taken')
        else:
            details.insert_one({"username":username,"password":password})
            flash('User successfully created')
        return render_template("form.html")
    else:
        return render_template("form.html")

if __name__ == '__main__':  
    app.run(debug = True)  
