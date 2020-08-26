import logging
# from bson.objectid import ObjectId
# from bson.errors import InvalidId
import uuid
from typing import List
from pymongo import IndexModel
from pymongo.collation import Collation, CollationStrength

DEFAULT_COLLATION = Collation(locale='en_US', strength=CollationStrength.SECONDARY)

class Dao(object):
    '''Interface for CRUD Serverice'''

    def create(self, doc):
        raise NotImplementedError

    def retrive(self, uid):
        raise NotImplementedError

    def retrieve_paged(self, skip, query=None, limit=10):
        raise NotImplementedError

    def update(self, doc):
        raise NotImplementedError

    def delete(self, uid):
        raise NotImplementedError


class UidInDictError(KeyError):
    pass


class MongoCollectionDao(Dao):

    ''' Mongo data service for mapping CRUD and search
    operations to a MongoDB. '''
    def __init__(self, db, collection_name, indexes: List[IndexModel] = None):
        self._db = db
        self._collection = db[collection_name]
        if indexes:
            self._collection.create_indexes(indexes)

    def create(self, doc):
        logging.debug(f"create doc in collection {0}, doc: {1}", self._collection, doc)
        if 'uid' in doc:
            raise UidInDictError('Document should not have uid field')
        uid = uuid.uuid4()
        doc['uid'] = str(uid)
        self._collection.insert_one(doc)
        return doc['uid']

    def retrieve(self, uid):
        return self._collection.find_one({"uid": uid}, {'_id': False})

    def retrieve_paged(self, skip=None, query=None, limit=10):
        if skip is not None:
            # Skip and limit
            cursor = self._collection.find(query, {'_id': False}) \
                                            .skip(skip).limit(limit) 
                                            # .collation(DEFAULT_COLLATION)

            # Return documents
            return cursor

        else:
            return self._collection.find(query)

    # def retreive_many(self, query=None):
    #     from warnings import warn
    #     warn("this will be merged with retrieve_paged very soon!!")
    #     return self._collection.find(query)

    def update(self, doc):
        if 'uid' not in doc:
            raise BadIdError('No uid provided')
        # update_one might be more efficient, but kinda tricky
        status = self._collection.replace_one({"uid": doc['uid']}, doc)
        if status.modified_count == 0:
            raise ObjectNotFoundError

    def delete(self, uid):
        status = self._collection.delete_one({"uid": uid})
        if status.deleted_count == 0:
            raise ObjectNotFoundError

class ObjectNotFoundError(Exception):
    pass

class UidInDictError(KeyError):
    pass

class BadIdError(Exception):
    pass




