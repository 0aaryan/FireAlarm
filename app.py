from flask import Flask , render_template,request,url_for,redirect,flash
import pymongo 
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from sqlalchemy import false
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

client = pymongo.MongoClient("mongodb+srv://aryan:abc1234@clients.k7mgg9r.mongodb.net/?retryWrites=true&w=majority")
db = client["clients"]
details=db["details"]
 
app = Flask(__name__)

app.secret_key = 'abc'

def send_mail(id):
    from_id='alertfire017@gmail.com'
    conn =smtplib.SMTP('smtp.gmail.com',587)  
    type(conn)  
    conn.ehlo()  
    conn.starttls()  
    message = MIMEMultipart("alternative")
    message["Subject"] = "Fire Alert"
    message["From"] = from_id
    message["To"] = id
    #generate body of email
    text = "Fire has been detected in your house."
    msg = MIMEText(text, "plain")
    message.attach(msg)
    conn.login(from_id,'plvwflcdrmwiddsj')  
    conn.sendmail(from_id,id,message.as_string())  
    conn.quit()

def send_alert(id):
    token = "5399157129:AAFUTKCYkNqJlwa6oNXfNuDBqE1PBUFJsYM"
    chat_id = id
    alert_msg="🔥🔥Fire alert🔥🔥"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
       "chat_id": chat_id,
       "text": alert_msg
    }
    resp = requests.get(url, params=params)

    # Throw an exception if Telegram API fails
    resp.raise_for_status()

@app.route("/",methods=["POST","GET"])
def home():

    if request.method=="POST":
        print("POST")
        username=request.form["username"]
        mail=request.form["mail"]
        password=request.form["password"]
        print(username,password)
        if details.count_documents({"username":username}):
            flash('Username already taken')
        else:
            details.insert_one({"username":username,"password":password,"mail":mail})
            user=details.find_one({'username':username},{"_id":1,"username":1,"password":1})
            print(user["_id"])
            flash('User successfully created\nid:'+str(user['_id']))
        
        return render_template("form.html")
    else:
        return render_template("form.html")


@app.route("/sensordata/",methods=["POST","GET"])
def data():

    if request.method=="POST":
        mongoid=(request.form.get('mongoid'))
        temp=(request.form.get('temp'))
        humidity=(request.form.get('humidity'))
        gas=(request.form.get('gas'))
        flame=(request.form.get('fire'))
        alert=(request.form.get('alert'))
        details.update_one({'_id':ObjectId(mongoid)},
                            {'$set': {"Temperature":temp,
                                       "Humidity":humidity,
                                       "Gas":gas,
                                       "Flame":flame}}
                            ,False,False)
        print(temp+" "+alert)
        if alert=='1':
            user=details.find_one({'_id':ObjectId(mongoid)},{"clientId":1,"mail":1})
            try:
                for i in user['clientId']:
                    send_alert(i)
                    send_mail(user['mail'])
            except:
                print("No client id")


    return render_template("form.html")

if __name__ == '__main__':  
    app.run(debug = True)  


#{'api_key': '1', 'gas': 977, 'fire': 4095, 'humidity': 75.6, 'temperature': 28.3}