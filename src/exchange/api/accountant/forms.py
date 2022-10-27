from typing import Optional

from fastapi import Request
from dependency_injector.wiring import Provide, inject

from exchange.containers import Application
from exchange.datasource import Database
from decimal import Decimal


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
            for c in currencies:
                with db.connection() as conn:
                    conn.execute(
                        f"insert into \"Currency\"(code, data, rate_in, rate_out) values('{c[0]}', now(), {c[1]}, {c[2]} );"
                    )

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
                self.tables = conn.execute(f"select * from daily_currency_rate_view;").fetchall()
        except Exception:
            self.errors.append("Something went wrong")
