import os
import json

from pymongo        import MongoClient
from pymongo.errors import ConnectionFailure
from bson           import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)







class MongoLoader:
    def __init__(self):
        try:
            user            = os.environ.get('MONGO_USERNAME')
            password        = os.environ.get('MONGO_PASSWORD')
            host            = os.environ.get('MONGO_HOST')
            port            = os.environ.get('MONGO_PORT')
            db_name         = os.environ.get('MONGO_DB')
            db_collection   = os.environ.get('MONGO_COLLECTION')

            
            if user == '' and password == '':
                uri=f'mongodb://{host}:{port}'
            else:
                uri=f'mongodb://{user}:{password}@{host}:{int(port)}?authSource=admin'
            
            self.client             = MongoClient(uri)
            self.db                 = self.client[db_name] if db_name else None
            self.collection_name    = self.db[db_collection] if db_collection else None
            
        
        except ConnectionFailure:
            self.client = None
            raise ValueError("MongoDB connection failed.")

    def is_connected(self):
        return self.client is not None

    def set_database(self, db_name):
        self.db = self.client[db_name]

    def set_collection(self, collection_name):
        self.collection_name = self.db[collection_name]

    def insert_data(self, data):
        if self.db is None:
            raise ValueError("Database not set.")
        
        if self.collection_name is None:
            raise ValueError("Collection not set.")
        
        if isinstance(data, list):
            if len(data) == 0:
                return
            if isinstance(data[0], dict):
                self.collection_name.insert_many(data)
            else:
                data = [d.__dict__() for d in data]
                self.collection_name.insert_many(data)
        else:
            if isinstance(data, dict):
                self.collection_name.insert_one(data)
            else:
                self.collection_name.insert_one(data.__dict__())

    def get_data(self, query=None):
        if self.db is None:
            raise ValueError("Database not set.")
        
        if self.collection_name is None:
            raise ValueError("Collection not set.")
        
        if query is None:
            return list(self.collection_name.find())
        else:
            return list(self.collection_name.find(query))
        
    def delete_data(self, query=None):
        if self.db is None:
            raise ValueError("Database not set.")
        
        if self.collection_name is None:
            raise ValueError("Collection not set.")
        
        if query is None:
            self.collection_name.delete_many({})
        else:
            self.collection_name.delete_many(query)
    
    def export_database(self, filename="database.json"):
        if self.db is None:
            raise ValueError("Database not set.")
        
        if self.collection_name is None:
            raise ValueError("Collection not set.")
        
        data = list(self.collection_name.find())
        print(f"Exporting {len(data)} events to {filename}")
        data = JSONEncoder().encode(data)
        print(f"EXporting again {len(data)} events to {filename}")
        with open(filename, "w") as f:
            print(f"Exporting (third) {len(data)} events to {filename}")
            json.dump(data, f, indent=4)
    
    def is_empty(self):
        if self.db is None:
            raise ValueError("Database not set.")
        
        if self.collection_name is None:
            raise ValueError("Collection not set.")
        
        return self.collection_name.count_documents({}) == 0
    
    def close(self):
        self.client.close()
