from pymongo import MongoClient, IndexModel
from pymongo.collation import Collation, CollationStrength
from ..service.users_service import UsersService
from ..service.runs_service import RunsService
from ..service.compounds_service import CompoundsService
from ..service.teams_service import TeamsService
from splash.data.base import MongoCollectionDao, DEFAULT_COLLATION


class ServiceProvider():
    """ Provides a single interface for constructing services based on a database instance.
        This is used as a global for service reousrces like fastapi.
    """

    def __init__(self, db: MongoClient):
        uid_index = IndexModel([('uid', 1)], name='uid', unique=True)
        users_name_index = IndexModel([('given_name', 1), ('family_name', 1)],
                                    #   collation=DEFAULT_COLLATION,
                                      name='name')
        users_auth_index = IndexModel([
                    ('authenticators.issuer', 1), 
                    ('authenticators.sub', 1), 
                    ('authenticators.email', 1)], 
                    name="authenticators")
        self._users_service = UsersService(MongoCollectionDao(
                        db, 'users', [uid_index, users_name_index, users_auth_index]))
        self._compounds_service = CompoundsService(MongoCollectionDao(db, 'compounds'))
        self._runs_service = RunsService(None)
        self._teams_service = TeamsService(MongoCollectionDao(db, 'teams'))
    @property
    def users(self):
        return self._users_service

    @property
    def compounds(self):
        return self._compounds_service

    @property
    def runs(self):
        return self._runs_service

    @property
    def teams(self):
        return self._teams_service
