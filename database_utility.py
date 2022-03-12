import pymongo
from sqlalchemy import outerjoin

database_name = 'mailex_database'

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db           = mongo_client["database_name"]
email_db     = db['emails']


def insert_emails(emails):

    out = emails.to_json(orient= 'records', default_handler= str, indent= 4)

    print(type(out))

    email_db.insert_many(out)

    return out


# if __name__ == '__main__':

#     mylist = [
#   { "name": "Amy", "address": "Apple st 652"},
#   { "name": "Hannah", "address": "Mountain 21"},
#   { "name": "Michael", "address": "Valley 345"},
#   { "name": "Sandy", "address": "Ocean blvd 2"},
#   { "name": "Betty", "address": "Green Grass 1"},
#   { "name": "Richard", "address": "Sky st 331"},
#   { "name": "Susan", "address": "One way 98"},
#   { "name": "Vicky", "address": "Yellow Garden 2"},
#   { "name": "Ben", "address": "Park Lane 38"},
#   { "name": "William", "address": "Central st 954"},
#   { "name": "Chuck", "address": "Main Road 989"},
#   { "name": "Viola", "address": "Sideway 1633"}
# ]


# x = email_db.insert_many(mylist)