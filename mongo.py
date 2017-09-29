import pymongo

client = pymongo.MongoClient("mongodb://nilesh:akura@ds147544.mlab.com:47544/akura")
db =  client.akura
coll = db.phones

def insert(data):
    phone =  db.phones.find_one({'Model': data["Model"] })
    if phone is None :
        db.phones.insert(data, check_keys=False)
        return True
    else:
        print "Already Exists:"
        print  data["Model"]
        return check_pros_and_cons(data["Model"])


def check_pros_and_cons(name):
    pros = db.phone_pros_and_cons.find_one({'name':name})
    if pros is None :
        return True
    else:
        print "Pros and Cons Already Exists"
        return False
    
       
def save_additional_details(primary,secondary):

    db.phones_comparisons.insert(primary,check_keys=False)
    db.phones_comparisons.insert(secondary,check_keys=False)
    print "primary saved for: "+ primary["name"]      
       

def save_pros_and_cons(pros_and_cons):
    db.phone_pros_and_cons.insert(pros_and_cons)
    print "pros and cons saved for: "+ pros_and_cons["name"]
       