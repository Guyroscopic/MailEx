import pymongo
from sqlalchemy import outerjoin

database_name = 'mailex_database'

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db           = mongo_client[database_name]
email_db     = db['emails']


def insert_emails(emails):

    #Converting Dataframe to a list dictionaires
    records = emails.to_dict('r')

    #Stroing dictionaries in mongoDB
    email_db.insert_many(records)