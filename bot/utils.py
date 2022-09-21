


def validate(username,password,ID):
    import pymongo
    client = pymongo.MongoClient("mongodb+srv://aryan:abc1234@clients.k7mgg9r.mongodb.net/?retryWrites=true&w=majority")
    db = client["clients"]
    details=db["details"]
    user=details.find_one({'username':username},{"_id":0,"username":1,"password":1})
    msg=''
    if user==None:
        msg="User does not exist"
    else:
        if user['password']!=password:
            msg="Wrong password, Try again"
        else:
            msg="Successfully logined"
            details.update_one({"username":username},{'$push':{"clientId":ID}},upsert=True)
    return msg