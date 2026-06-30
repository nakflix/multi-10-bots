import pymongo


class Database:
    """
    One Database instance per bot. Each bot gets its own MongoClient,
    its own database, and its own 'users' collection - fully isolated
    from the other 9 bots even though the code is identical.
    """

    def __init__(self, db_uri: str, db_name: str):
        self.dbclient = pymongo.MongoClient(db_uri)
        self.database = self.dbclient[db_name]
        self.user_data = self.database['users']

    async def present_user(self, user_id: int) -> bool:
        found = self.user_data.find_one({'_id': user_id})
        return bool(found)

    async def add_user(self, user_id: int):
        self.user_data.insert_one({'_id': user_id})
        return

    async def full_userbase(self):
        user_docs = self.user_data.find()
        user_ids = []
        for doc in user_docs:
            user_ids.append(doc['_id'])
        return user_ids

    async def del_user(self, user_id: int):
        self.user_data.delete_one({'_id': user_id})
        return
