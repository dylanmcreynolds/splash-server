from fastapi import APIRouter, Path, Security, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, List, Optional
from pydantic import BaseModel
from splash.models.users import UserModel
from splash.service.runs_service import CatalogDoesNotExist, FrameDoesNotExist, BadFrameArgument
from splash.api import get_service_provider as services
from .auth import get_current_user

router = APIRouter()


class RunModel(BaseModel):
    uid: str
    num_images: int
    sample_name: str


class RunMetadataModel(BaseModel):
    energy: float


@router.get("", tags=["runs"], response_model=List[str])
def read_catalogs(
        current_user: UserModel = Security(get_current_user)):

    catalog_names = services().runs.list_root_catalogs()
    return catalog_names


@router.get("/{catalog_name}", tags=['runs'], response_model=List[RunModel])
def read_catalog(
            catalog_name: str = Path(..., title="name of catalog"),
            current_user: UserModel = Security(get_current_user)):
    try:
        runs = services().runs.get_runs(current_user, catalog_name)
    except CatalogDoesNotExist as e:
        raise HTTPException(404, detail=e.args[0])

    return_runs = []
    for run in runs:
        return_run = RunModel(
                           uid=run.get('uid'),
                           num_images=run.get('num_images'),
                           sample_name=run.get('/entry/sample/name'))
        return_runs.append(return_run)
    return return_runs


@router.get("/{catalog_name}/{run_uid}/image", tags=['runs'], response_model=RunModel)
def read_frame(
        catalog_name: str = Path(..., title="catalog name"),
        run_uid: str = Path(..., title="run uid"),
        frame: Optional[int] = 0,
        current_user: UserModel = Security(get_current_user)):
    try:
        jpeg_generator = services().runs.get_image(catalog_name=catalog_name, uid=run_uid, frame=frame)
    except FrameDoesNotExist as e:
        raise HTTPException(400, detail=e.args[0])
    except BadFrameArgument as e:
        raise HTTPException(422, detail=e.args[0])

    return StreamingResponse(jpeg_generator, media_type="image/JPEG")


@router.get("/{catalog_name}/{run_uid}/metadata", tags=['runs'], response_model=RunMetadataModel)
def read_frame_metadata(
        catalog_name: str = Path(..., title="catalog name"),
        run_uid: str = Path(..., title="run uid"),
        frame: Optional[int] = 0):
    try:
        return_metadata = services().runs.get_metadata(catalog_name=catalog_name, uid=run_uid, frame=frame)
    except FrameDoesNotExist as e:
        raise HTTPException(400, detail=e.args[0])
    except BadFrameArgument as e:
        raise HTTPException(422, detail=e.args[0])

    return RunMetadataModel(energy=return_metadata.get('/entry/instrument/monochromator/energy'))
