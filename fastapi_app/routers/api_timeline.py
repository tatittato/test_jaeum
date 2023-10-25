from fastapi import APIRouter

router = APIRouter(
    tags=["Timeline"],
    responses={404: {"description": "Not found"}},
)