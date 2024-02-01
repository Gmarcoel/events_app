from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoLoader:
    def __init__(self, host='mongo_db', port=27017, user='', password='', db_name=None, collection_name=None):
        try:
            if user == '' and password == '':
                uri=f'mongodb://{host}:{port}'
            else:
                uri=f'mongodb://{user}:{password}@{host}:{port}?authSource=admin'
            self.client = MongoClient(uri)
            self.db = self.client[db_name] if db_name else None
            self.collection_name = self.db[collection_name] if collection_name else None
            
        
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
            data = [d.__dict__() for d in data]
            self.collection_name.insert_many(data)
        else:
            self.collection_name.insert_one(data.__dict__())

    def get_data(self, query=None):
        if self.db is None:
            raise ValueError("Database not set.")
        
        if self.collection_name is None:
            raise ValueError("Collection not set.")
        
        if query is None:
            return self.collection_name.find()
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
    

    def close(self):
        self.client.close()