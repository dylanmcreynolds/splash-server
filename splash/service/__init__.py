from pymongo import MongoClient
from ..service.base import Service
from ..service.users_service import UsersService
from ..service.runs_service import RunsService
from ..service.compounds_service import CompoundsService
from splash.data.base import MongoCollectionDao


class ServiceProvider():
    """ Provides a single interface for constructing services based on a database instance.
        This is used as a global for service reousrces like fastapi.
    """

    def __init__(self, db: MongoClient):
        self._users_service = UsersService(MongoCollectionDao(db, 'users'))
        self._compounds_service = CompoundsService(MongoCollectionDao(db, 'compounds'))
        self._runs_service = RunsService()
        self._ingest_mappings_service = Service(MongoCollectionDao(db, 'ingest_mappings'))

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
    def ingest_mappings(self):
        return self._ingest_mappings_service
