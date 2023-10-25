from fastapi import APIRouter

router = APIRouter(
    tags=["Statistics"],
    responses={404: {"description": "Not found"}},
)