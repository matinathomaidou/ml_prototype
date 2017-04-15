import pymongo
from bson import ObjectId
import config


uri = config.uri

DATABASE = "mlexperience"


class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient(uri)
        self.db = client[DATABASE]

    def get_user(self, email):
        return self.db.users.find_one({"email": email})

    def add_user(self, email, salt, hashed, is_admin):
        self.db.users.insert({"email": email, "salt": salt, "hashed": hashed, "admin": is_admin})
        
    def list_user(self):
        users = []
        for user in self.db.users.find():
            users.append(user)
        return users
        
    def del_user(self, email):
        self.db.users.remove({"email": email})
        

    def pw_user_update(self, email, salt, hashed, is_admin):
        self.db.users.update({"email": email}, {"$set": {"salt": salt, "hashed":hashed}})
      

    def add_table(self, number, owner):
        new_id = self.db.tables.insert({"number": number, "owner": owner})
        return new_id

    def update_table(self, _id, url):
        self.db.tables.update({"_id": _id}, {"$set": {"url": url}})

    def get_tables(self, owner_id):
        return list(self.db.tables.find({"owner": owner_id}))

    def get_table(self, table_id):
        return self.db.tables.find_one({"_id": ObjectId(table_id)})

    def delete_table(self, table_id):
        self.db.tables.remove({"_id": ObjectId(table_id)})

    def add_request(self, table_id, time):
        table = self.get_table(table_id)
        try:
            self.db.requests.insert({"owner": table['owner'], "table_number": table[
                                    'number'], "table_id": table_id, "time": time})
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    def get_requests(self, owner_id):
        return list(self.db.requests.find({"owner": owner_id}))

    def delete_request(self, request_id):
        self.db.requests.remove({"_id": ObjectId(request_id)})
        