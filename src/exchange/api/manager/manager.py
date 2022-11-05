from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from exchange.api.auth.session import SessionData, cookie, verifier
from exchange.api.manager.forms import AddCashAmountForm, GetCashAmountForm, CreateUser, SaveUser, GetUsers, DelUser

router = APIRouter(tags=["Manager"])
templates = Jinja2Templates(directory="templates")


@router.get("/manager/add-cash-amount", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def get_form(request: Request, session_data: SessionData = Depends(verifier)):
    response_dict = {"request": request, "errors": []}
    response_dict.update(session_data.user)
    return templates.TemplateResponse("manager/add_cash_amount.html", response_dict)


@router.post("/manager/add-cash-amount", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def add_client(request: Request, session_data: SessionData = Depends(verifier)):
    form = AddCashAmountForm(request)
    await form.load_data()
    form.save()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("manager/add_cash_amount.html", form.__dict__)


@router.get("/manager/get-cash-amount", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def get_by_passport(request: Request, session_data: SessionData = Depends(verifier)):
    form = GetCashAmountForm(request)
    form.get()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("manager/get_cash_amount.html", form.__dict__)


@router.get("/manager/add-user", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def add_user(request: Request, session_data: SessionData = Depends(verifier)):
    form = CreateUser(request)
    form.get()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("manager/add_user.html", form.__dict__)


@router.post("/manager/add-user", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def save_user(request: Request, session_data: SessionData = Depends(verifier)):
    form = SaveUser(request)
    await form.load_data()
    form.save()
    users_form = GetUsers(request)
    users_form.get()
    form.__dict__.update(users_form.__dict__)
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("manager/users.html", form.__dict__)


@router.get("/manager/users", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def users(request: Request, session_data: SessionData = Depends(verifier)):
    form = GetUsers(request)
    form.get()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("manager/users.html", form.__dict__)

@router.post("/manager/del-user/{email}", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def users(email: str, request: Request, session_data: SessionData = Depends(verifier), ):
    form = DelUser()
    form.delete(email)
    form = GetUsers(request)
    form.get()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("manager/users.html", form.__dict__)
