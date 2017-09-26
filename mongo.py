import pymongo

client = pymongo.MongoClient("mongodb://nilesh:akura@ds147544.mlab.com:47544/akura")
db =  client.akura
coll = db.phones

def insert(data):
    phone =  coll.find_one({'Model': data["Model"] })
    if phone is None :
        coll.insert(data, check_keys=False)
    else:
        print "Already Exists"
    
       
       
       

