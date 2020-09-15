
from collections import namedtuple
from splash.models.users import UserModel

from splash.data.base import MongoCollectionDao

ValidationIssue = namedtuple('ValidationIssue', 'description, location, exception')


class BadPageArgument(Exception):
    pass


class Service():

    def __init__(self, dao: MongoCollectionDao):
        self.dao = dao


    def create(self, current_user: UserModel, data):
        return self.dao.create(data)

    def retrieve_one(self, current_user: UserModel, uid):
        return self.dao.retrieve(uid)

    def retrieve_multiple(self,
                          current_user: UserModel,
                          skip: int = None,
                          query=None,
                          limit=10):

        if skip < 0:
            raise BadPageArgument("Page parameter must be positive")
        cursor = self.dao.retrieve_paged(skip=skip, query=query, limit=0)
        return list(cursor)
        # return 

    def update(self, current_user: UserModel, data, uid: str):
        return self.dao.update(data, uid)

    def delete(self, current_user: UserModel, uid):
        raise NotImplementedError()
