from splash.data.base import MongoCollectionDao
from splash.service.base import Service


class TeamsService(Service):

    def __init__(self, dao: MongoCollectionDao):
        super().__init__(dao)
        self.dao = dao
