from fastapi import APIRouter,  Security
from typing import List, Optional
from pydantic import parse_obj_as, BaseModel

from splash_ingest.model import Mapping
from splash.models.users import UserModel
from splash.api import get_service_provider as services
from .auth import get_current_user

router = APIRouter()


class IngestMapping(Mapping):
    uid: Optional[str] = None


class CreateIngestResponse(BaseModel):
    uid: str


@router.get("", tags=["ingest mappings"], response_model=List[IngestMapping])
def read_compounds(current_user: UserModel = Security(get_current_user)):
    compounds = services().ingest_mappings.retrieve_multiple(current_user, 1)
    results = parse_obj_as(List[IngestMapping], compounds)
    return results


@router.get("/{uid}", tags=['ingest mappings'])
def read_compound(
        uid: str,
        current_user: UserModel = Security(get_current_user)):

    mappings_dict = services().ingest_mappings.retrieve_one(current_user, uid)
    return (IngestMapping(**mappings_dict))

@router.put("/{uid}", tags=['ingest mappings'], response_model=CreateIngestResponse)
def replace_compound(
        uid: str,
        mapping: IngestMapping,
        current_user: UserModel = Security(get_current_user)):
    uid = services().ingest_mappings.update(current_user, mapping.dict(), uid)
    return CreateIngestResponse(uid=uid)


@router.post("", tags=['ingest mappings'], response_model=CreateIngestResponse)
def create_compound(
        new_compound: IngestMapping,
        current_user: UserModel = Security(get_current_user)):
    uid = services().ingest_mappings.create(current_user, new_compound.dict())
    return CreateIngestResponse(uid=uid)
