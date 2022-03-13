import pymongo

database_name = 'mailex'

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db           = mongo_client[database_name]
email_db     = db['emails']


def insert_emails(emails):

    #Converting Dataframe to a list dictionaires
    records = emails.to_dict('r')

    #Stroing dictionaries in mongoDB
    email_db.insert_many(records)


def get_num_read_emails():

    return db['num_read_emails'].find()[0]['num_read_emails']


def set_num_read_emails(new_value):

    collection  = db['num_read_emails']
    old         = collection.find()[0]
    new         = { "$set": { "num_read_emails": new_value } }

    collection.update_one(old, new)
 