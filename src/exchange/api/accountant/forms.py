import datetime
from decimal import Decimal, localcontext
from typing import Optional, Any

from dependency_injector.wiring import Provide, inject
from fastapi import Request
from sqlalchemy import select, func
from sqlalchemy.engine import RowProxy

from exchange.containers import Application
from exchange.datasource import Database
from exchange.infrastructure.views import daily_currency_rate_view, deal_report_view, monthly_currency_amounts
from exchange.infrastructure.views.compensation_view import compensation_view


class AddCurrencyRateForm:
    currencies = ["USD", "EUR", "JPY", "GBP", "CHF"]

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg = []
        self.usd_rate_in: Optional[Decimal] = None
        self.usd_rate_out: Optional[Decimal] = None
        self.eur_rate_in: Optional[Decimal] = None
        self.eur_rate_out: Optional[Decimal] = None
        self.gbp_rate_in: Optional[Decimal] = None
        self.gbp_rate_out: Optional[Decimal] = None
        self.jpy_rate_in: Optional[Decimal] = None
        self.jpy_rate_out: Optional[Decimal] = None
        self.chf_rate_in: Optional[Decimal] = None
        self.chf_rate_out: Optional[Decimal] = None

    async def load_data(self):
        try:
            form = await self.request.form()
            self.usd_rate_in = Decimal(form.get("usd_rate_in")) if form.get("usd_rate_in") else None
            self.usd_rate_out = Decimal(form.get("usd_rate_out")) if form.get("usd_rate_out") else None
            self.eur_rate_in = Decimal(form.get("eur_rate_in")) if form.get("eur_rate_in") else None
            self.eur_rate_out = Decimal(form.get("eur_rate_out")) if form.get("eur_rate_out") else None
            self.gbp_rate_in = Decimal(form.get("gbp_rate_in")) if form.get("gbp_rate_in") else None
            self.gbp_rate_out = Decimal(form.get("gbp_rate_out")) if form.get("gbp_rate_out") else None
            self.jpy_rate_in = Decimal(form.get("jpy_rate_in")) if form.get("jpy_rate_in") else None
            self.jpy_rate_out = Decimal(form.get("jpy_rate_out")) if form.get("jpy_rate_out") else None
            self.chf_rate_in = Decimal(form.get("chf_rate_in")) if form.get("chf_rate_in") else None
            self.chf_rate_out = Decimal(form.get("chf_rate_out")) if form.get("chf_rate_out") else None
        except Exception:
            self.errors.append("Added wrong rate")

    @inject
    def save(self, db: Database = Provide[Application.datasources.postgres]):
        currencies = []
        for code in self.currencies:
            rate = [code]
            for key in self.__dict__:
                if code.lower() in key and "in" in key:
                    rate.append(self.__dict__[key])
            for key in self.__dict__:
                if code.lower() in key and "out" in key:
                    rate.append(self.__dict__[key])
            currencies.append(rate)
        try:
            for curr in currencies:
                with db.connection() as conn:
                    conn.execute(f"call add_currency_rate('{curr[0]}', {curr[1]}, {curr[2]});")

            self.msg.append("Currencies added")
        except Exception:
            self.errors.append("Something went wrong")


class ShowCurrencyRatesForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.tables: Optional[list] = None

    @inject
    def get_currency_rates(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                self.tables = conn.execute(select([daily_currency_rate_view])).fetchall()
        except Exception:
            self.errors.append("Something went wrong")


class GetMonthlyCompensation:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.data: Optional[list] = None
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @inject
    def get_currency_rates(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                self.data = conn.execute(select([compensation_view])).fetchall()
        except Exception:
            self.errors.append("Something went wrong")


class MonthlyReport:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.deal_data: Optional[list] = None
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.currency_data: list[dict[str, Any]] = []

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                self.deal_data = conn.execute(select([deal_report_view])).fetchall()
                self._get_currency_report(conn.execute(select([monthly_currency_amounts])).fetchall())
        except Exception:
            self.errors.append("Something went wrong")

    def _get_currency_report(self, raw_data: list[RowProxy]) -> None:
        all_sold_currencies_amount = sum([a.sold_amount for a in raw_data if a.sold_amount])
        all_bought_currencies_amount = sum([a.bought_amount for a in raw_data if a.bought_amount])
        for currency_code in ["USD", "EUR", "JPY", "GBP", "CHF", "BYN"]:
            for data in raw_data:
                if data.bcode == currency_code or data.scode == currency_code:
                    sold_amount = data.sold_amount if data.sold_amount else "-"
                    bought_amount = data.bought_amount if data.bought_amount else "-"
                    sell_percent = (
                        round(sold_amount * 100 / all_sold_currencies_amount, 2)
                        if isinstance(sold_amount, float)
                        else "-"
                    )
                    buy_percent = (
                        round(bought_amount * 100 / all_bought_currencies_amount, 2)
                        if isinstance(bought_amount, float)
                        else "-"
                    )
                    self.currency_data.append(
                        {
                            "code": currency_code,
                            "sold_amount": sold_amount,
                            "bought_amount": bought_amount,
                            "sell_percent": sell_percent,
                            "buy_percent": buy_percent,
                        }
                    )
