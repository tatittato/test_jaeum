from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["Web Pages"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")

@router.get("/statistics")
def chart(request: Request):

    return templates.TemplateResponse("statistics.html", {"request": request})
