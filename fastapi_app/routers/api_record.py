from fastapi import APIRouter

router = APIRouter(
    tags=["Record"],
    responses={404: {"description": "Not found"}},
)