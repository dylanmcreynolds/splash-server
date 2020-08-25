from enum import Enum
from typing import List
from ..models.teams import Team
from ..models.users import UserModel


class Action(Enum):
    CREATE = "create"
    RETRIEVE = "RETRIEVE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Checker():

    def can_do(self, user: UserModel, resource, action) -> bool:
        raise NotImplementedError()


class TeamRunChecker(Checker):
    def __init__(self, teams: List[Team]):
        super().__init__()
        self._teams = teams

    def get_user_teams(self, user: UserModel) -> List[Team]:
        """returns a list of Teams that the 
        user has membership in, including all roles

        Parameters
        ----------
        user : UserModel

        Returns
        -------
        List[Team]

        """
        for team in self._teams:
            if user.uid in team.members:
                yield team

    def can_do(self, user: UserModel, run, action: Action):
        if action == Action.RETRIEVE:
            # This rule is simple...check if the user
            # is a member the team that matches the run
            for team in self.get_user_teams(user):
                if team.name == run['team']:
                    return True
        return False


class MongoTeamRunChecker(Checker):

    def __init__(self, db):
        self._db = db
        self._teams = None

