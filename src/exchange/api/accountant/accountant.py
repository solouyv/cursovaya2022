from dependency_injector.wiring import inject
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from exchange.api.accountant.forms import AddCurrencyRateForm, ShowCurrencyRatesForm
from exchange.api.auth.session import SessionData, cookie, verifier

router = APIRouter(tags=["Accountant"])
templates = Jinja2Templates(directory="templates")


@router.get("/accountant/add-currency-rate", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def get_form(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    response_dict = {"request": request, "errors": []}
    response_dict.update(session_data.user)
    return templates.TemplateResponse("accountant/add_currency_rate.html", response_dict)


@router.post("/accountant/add-currency-rate", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def add_data(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = AddCurrencyRateForm(request)
    await form.load_data()
    form.save()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("accountant/add_currency_rate.html", form.__dict__)


@router.get("/accountant/add-data-to-office-table", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def show_currency_rates(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    form = ShowCurrencyRatesForm(request)
    form.get_currency_rates()
    form.__dict__.update(session_data.user)
    return templates.TemplateResponse("accountant/office_table.html", form.__dict__)


@router.get("/accountant/monthly-report", response_class=HTMLResponse, dependencies=[Depends(cookie)])
@inject
async def get_form(
    request: Request,
    session_data: SessionData = Depends(verifier)
):
    response_dict = {"request": request, "errors": []}
    response_dict.update(session_data.user)
    return templates.TemplateResponse("accountant/monthly_report.html", response_dict)
