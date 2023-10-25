from fastapi import APIRouter

router = APIRouter(
    tags=["Score"],
    responses={404: {"description": "Not found"}},
)