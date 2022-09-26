import pymongo

class MongoWrapper:

    def __init__(self, DB_USERID_MONGO, DB_PASSWORD_MONGO, DB_HOST_MONGO, DB_PORT_MONGO, DB_AUTH_NM_MONGO):

        self.settings_mongo = {
            'username': DB_USERID_MONGO,
            'password': DB_PASSWORD_MONGO,
            'host': DB_HOST_MONGO + ":" + DB_PORT_MONGO,
            'database': DB_AUTH_NM_MONGO
        }

        self.mongo_client =\
            MongoClient("mongodb://{username}:{password}@"
                        "{host}/?authSource={database}".format(
                            **self.settings_mongo))

    def execute_operation(self, db_name, collection_name, query,
                          operation):
        assert operation in ["find", "find_one", "distinct"]
        db = self.mongo_client[db_name]
        collection = db[collection_name]
        rs = getattr(collection, operation)(query)
        return rs

    def find_one(self, db_name, collection_name, query):
        return self.execute_operation(self, db_name, collection_name, query,
                                      operation="find_one")

    def find(self, db_name, collection_name, query):
        TODO

    def delete(self, db_name, collection_name, query):
        TODO

    def ensure_index_if_not_exist(self, db_name, collection_name, query):
        TODO

    def distinct(self, db_name, collection_name, query):
        TODO

    def insert(self, db_name, collection_name, query):
        TODO

    def update(self, db_name, collection_name, query):
        TODO