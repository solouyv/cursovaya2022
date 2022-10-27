from uuid import uuid4, UUID

from dependency_injector.wiring import inject
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from exchange.api.auth import LoginForm
from exchange.api.auth.session import SessionData, backend, cookie, verifier

router = APIRouter(tags=["Exchange"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
@inject
def start(
    request: Request,
):
    return templates.TemplateResponse("main.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        session = uuid4()
        data = SessionData(user=form.user_dict)
        await backend.create(session, data)
        response_dict = {"request": request}
        response_dict.update(form.user_dict)
        response = templates.TemplateResponse("main.html", response_dict)
        cookie.attach_to_response(response, session)
        return response
    return templates.TemplateResponse("main.html", {"request": request, "errors": form.errors})


@router.get("/main", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def start(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    response_dict = {"request": request, "errors": []}
    response_dict.update(session_data.user)
    return templates.TemplateResponse("main.html", response_dict)


@router.delete("/")
async def del_session(request: Request, session_id: UUID = Depends(cookie)):
    response = templates.TemplateResponse("main.html", {"request": request, "user": None})
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return response
