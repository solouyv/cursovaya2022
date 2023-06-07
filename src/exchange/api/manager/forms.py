from decimal import Decimal
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Request
from sqlalchemy import select, func

from exchange.containers import Application
from exchange.datasource import Database
from exchange.infrastructure.views import (
    byn_currency_view,
    daily_currency_rate_view, daily_cash_amount, roles_view, salaries_view, user_with_roles_view,
)


class AddCashAmountForm:
    currencies = ["USD", "EUR", "JPY", "GBP", "CHF"]

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg = []
        self.usd: Optional[Decimal] = None
        self.eur: Optional[Decimal] = None
        self.gbp: Optional[Decimal] = None
        self.jpy: Optional[Decimal] = None
        self.chf: Optional[Decimal] = None
        self.byn: Optional[Decimal] = None

    async def load_data(self):
        try:
            form = await self.request.form()
            self.usd = Decimal(form.get("usd"))
            self.eur = Decimal(form.get("eur"))
            self.gbp = Decimal(form.get("gbp"))
            self.jpy = Decimal(form.get("jpy"))
            self.chf = Decimal(form.get("chf"))
            self.byn = Decimal(form.get("byn"))
        except Exception:
            self.errors.append("Added wrong data")

    @inject
    def save(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                conn.execute(f"call truncate_daily_cash_amount();")
                byn_data = conn.execute(select([byn_currency_view])).fetchone()
                conn.execute(f"call add_cash_amount('{byn_data.id}', '{self.byn}');")
                currency_ids = {c.code: c.id for c in conn.execute(select([daily_currency_rate_view])).fetchall()}
                for c in self.currencies:
                    conn.execute(f"call add_cash_amount('{currency_ids[c]}', '{self.__dict__.get(c.lower())}');")
            self.msg.append("Cash amount added")
        except Exception:
            self.errors.append("Something went wrong")


class GetCashAmountForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.currencies: Optional[list[dict]] = None

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                self.currencies = conn.execute(select([daily_cash_amount])).fetchall()
        except Exception:
            self.errors.append("Something went wrong")
        return self


class CreateUser:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.roles: Optional[list[dict]] = None
        self.salaries: Optional[list[dict]] = None

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                self.roles = conn.execute(select([roles_view])).fetchall()
                self.salaries = conn.execute(select([salaries_view])).fetchall()
        except Exception:
            self.errors.append("Something went wrong")
        return self


class SaveUser:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []

    async def load_data(self):
        try:
            form = await self.request.form()
            self.first_name = form.get("first_name")
            self.last_name = form.get("last_name")
            self.emali = form.get("email")
            self.password = form.get("password")
            self.role_id = int(form.get("role_id"))
            self.salary_level = int(form.get("salary_level"))
            self.salary_increase = True if form.get("salary_increase") else False

        except Exception:
            self.errors.append("Added wrong data")

    @inject
    def save(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                conn.execute(
                    "{} {}".format(
                        f"call add_user('{self.emali}', '{self.first_name}', '{self.last_name}',",
                        f"'{self.password}', '{self.role_id}', '{self.salary_level}', '{self.salary_increase}');"
                    )
                )
                self.msg.append("User added")
        except Exception:
            self.errors.append("Something went wrong")
        return self


class GetUsers:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.users: Optional[list[dict]] = None

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                self.users = conn.execute(select([user_with_roles_view])).fetchall()
                self.users = [u for u in sorted(self.users, key=lambda x: x.user)]
        except Exception:
            self.errors.append("Something went wrong")
        return self


class DelUser:
    def __init__(self):
        self.errors: list = []
        self.msg: list = []

    @inject
    def delete(self, email: str, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                conn.execute(func.public.del_user(email))
                self.msg.append("User deleted")
        except Exception:
            self.errors.append("Something went wrong")
        return self
