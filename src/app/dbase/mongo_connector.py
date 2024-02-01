from pymongo import MongoClient
import os

def get_db():
    mongo_username = os.environ.get('MONGO_USERNAME')
    mongo_password = os.environ.get('MONGO_PASSWORD')
    mongo_host = os.environ.get('MONGO_HOST')
    mongo_port = os.environ.get('MONGO_PORT')
    mongo_db = os.environ.get('MONGO_DB')

    if mongo_username is None or mongo_password is None:
        raise ValueError("MongoDB username or password not set.")
    
    
    uri=f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{int(mongo_port)}?authSource=admin'
    client = MongoClient(uri)
    db = client[mongo_db] if mongo_db else None

    return db

def get_all_events():
    db = get_db()
    if db is None:
        raise ValueError("Database connection not established.")
    collection = db['events']
    return list(collection.find({}))