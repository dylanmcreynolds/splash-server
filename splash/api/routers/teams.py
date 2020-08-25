from fastapi import APIRouter, Security
# from fastapi.security import OpenIdConnect
from pydantic import BaseModel
from typing import List
from splash.models.users import UserModel
from splash.models.teams import Team, NewTeam
from splash.api import get_service_provider as services
from .auth import get_current_user

router = APIRouter()


class CreateTeamResponse(BaseModel):
    uid: str


@router.get("/", tags=["teams"], response_model=List[Team])
def read_teams(
            current_user: UserModel = Security(get_current_user)):
    results = services().teams.retrieve_multiple(current_user, 1)
    return results


@router.get("/{uid}", tags=['teams'], response_model=Team)
def read_team(
            uid: str,
            current_user: UserModel = Security(get_current_user)):
    user_json = services().teams.retrieve_one(current_user, uid)
    return (Team(**user_json))


@router.post("/", tags=['teams'], response_model=CreateTeamResponse)
def create_team(
                team: NewTeam,
                current_user: UserModel = Security(get_current_user)):
    uid = services().teams.create(current_user, team.dict())
    return CreateTeamResponse(uid=uid)
