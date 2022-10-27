from dependency_injector.wiring import inject
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from exchange.api.auth.session import SessionData, cookie, verifier
from exchange.api.teller.forms import AddCustomerForm, GetPassportIdsForm, CreatDealForm, SaveDealForm, GetCardIdsForm

router = APIRouter(tags=["Teller"])
templates = Jinja2Templates(directory="templates")


@router.get("/teller/add-client", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def get_form(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    response_dict = {"request": request, "errors": []}
    response_dict.update(session_data.user)
    return templates.TemplateResponse("teller/add_client.html", response_dict)


@router.post("/teller/add-client", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def add_client(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = AddCustomerForm(request)
    await form.load_data()
    form.save()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("teller/add_client.html", form.__dict__)


@router.get("/teller/get-by-passport-id", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def get_by_passport(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = GetPassportIdsForm(request)
    form.get()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("teller/get_by_passport_id.html", form.__dict__)


@router.post("/teller/creat-deal", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def create_deal(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = CreatDealForm(request)
    await form.load_data()
    form.get()
    if not form.errors:
        form.__dict__.update(session_data.user)
        return templates.TemplateResponse("teller/create_deal.html", form.__dict__)
    old_form = GetPassportIdsForm(request).get()
    old_form.errors = form.errors
    old_form.__dict__.update(session_data.user)
    return templates.TemplateResponse("teller/get_by_passport_id.html", old_form.__dict__)


@router.post("/teller/save-deal", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def save_deal(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = SaveDealForm(request)
    await form.load_data(session_data.user)
    form.validate()
    form.save()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("teller/create_deal.html", form.__dict__)


@router.get("/teller/get-by-card-id", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
def get_by_passport(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = GetCardIdsForm(request)
    form.get()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("teller/get_by_card_id.html", form.__dict__)
