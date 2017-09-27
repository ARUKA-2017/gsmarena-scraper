import pymongo

client = pymongo.MongoClient("mongodb://nilesh:akura@ds147544.mlab.com:47544/akura")
db =  client.akura
coll = db.phones

def insert(data):
    phone =  db.phones.find_one({'Model': data["Model"] })
    if phone is None :
        db.phones.insert(data, check_keys=False)
    else:
        print "Already Exists"
    
       
def save_additional_details(primary,secondary):

    db.phones_comparisons.insert(primary,check_keys=False)
    db.phones_comparisons.insert(secondary,check_keys=False)
    print "primary saved for: "+ primary["name"]      
       

def save_pros_and_cons(pros_and_cons):
    db.phone_pros_and_cons.insert(pros_and_cons)
    print "pros and cons saved for: "+ pros_and_cons["name"]
       