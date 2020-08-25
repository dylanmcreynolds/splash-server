from typing import Dict, List
from pydantic import BaseModel


class Team(BaseModel):
    name: str
    members: Dict[str, List[str]]  # uid, role


class NewTeam(Team):
    uid: str
