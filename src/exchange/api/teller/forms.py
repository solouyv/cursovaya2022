import uuid
from decimal import Decimal
from typing import Optional, Any

from fastapi import Request
from dependency_injector.wiring import Provide, inject

from exchange.containers import Application
from exchange.datasource import Database


class AddCustomerForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg = []
        self.first_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.passport_id: Optional[str] = None
        self.bank_card: Optional[str] = None

    async def load_data(self):
        try:
            form = await self.request.form()
            self.first_name = form.get("first_name")
            self.last_name = form.get("last_name")
            self.passport_id = form.get("passport_id")
            self.bank_card = form.get("bank_card")
        except Exception:
            self.errors.append("Added wrong data")

    @inject
    def save(self, db: Database = Provide[Application.datasources.postgres]):
        bank_card_id = str(uuid.uuid4()) if self.bank_card else "null"
        try:
            with db.connection() as conn:
                conn.execute(
                    (
                        f"insert into \"Customer\"(first_name, last_name, passport_id, bank_card_id)"
                        f" values('{self.first_name}', '{self.last_name}', '{self.passport_id}', '{bank_card_id}');"
                    )
                )
            self.msg.append("Customer added")
        except Exception:
            self.errors.append("Customer already exists")


class GetPassportIdsForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.passport_ids: Optional[list[str]] = None

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                res = conn.execute(f"select \"passport_id\" from \"Customer\";").fetchall()
        except Exception:
            self.errors.append("Something went wrong")
        self.passport_ids = sorted([id_[0] for id_ in res])
        return self


class GetCardIdsForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.card_ids: Optional[list[str]] = None

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                res = conn.execute(f"select * from get_card_ids;").fetchall()
        except Exception:
            self.errors.append("Something went wrong")
        self.card_ids = sorted([id_[0] for id_ in res])
        return self


class CreatDealForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []
        self.passport_id: Optional[str] = None
        self.passport_id_from_list: Optional[str] = None
        self.customer_data: Optional[dict[str, Any]] = None
        self.daily_currency_rate_view: dict[str, Any] = {}

    async def load_data(self):
        try:
            form = await self.request.form()
            self.passport_id = form.get("passport_id")
            self.passport_id_from_list = form.get("passport_id_from_list")
        except Exception:
            self.errors.append("Added wrong data")

    @inject
    def get(self, db: Database = Provide[Application.datasources.postgres]):
        passport_id = self.passport_id or self.passport_id_from_list
        try:
            with db.connection() as conn:
                byn_data = dict(conn.execute(f"select * from \"Currency\" where \"id\" = 1;").fetchone())
                self.daily_currency_rate_view.update({byn_data["code"]: byn_data})
                [
                    self.daily_currency_rate_view.update({d.code: dict(d)})
                    for d in conn.execute("select * from \"daily_currency_rate_view\"").fetchall()
                ]
                res = conn.execute(f"select * from \"Customer\" where \"passport_id\" = '{passport_id}' ;").fetchone()
                self.customer_data = dict(res) if res else None
                if not self.customer_data:
                    self.errors.append(f"There isn't such client")
        except Exception:
            self.errors.append("Something went wrong")


class SaveDealForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.msg: list = []

    async def load_data(self, user):
        try:
            form = await self.request.form()
            self.customer_id = int(form.get("customer_id"))
            self.user_id = int(user["user_id"])
            self.currency_in_id = int(form.get("currency_for_purchasing"))
            self.currency_out_id = int(form.get("currency_for_sale"))
            self.daily_currency_rate_view = {}
            self.currency_in_count = Decimal(form.get("currency_amount"))
        except Exception:
            self.errors.append("Added wrong data")

    def validate(self) -> None:
        import ipdb;
        ipdb.set_trace()
        if not self.errors:
            if self.currency_in_id == self.currency_out_id:
                self.errors.append("The same currencies for sale and purchasing")
            elif self.currency_in_count <= 0:
                self.errors.append("Currency amount for purchasing should be more than 0")

    @inject
    def save(self, db: Database = Provide[Application.datasources.postgres]):
        try:
            with db.connection() as conn:
                if not self.errors:
                    conn.execute(
                        f"call \"add_deal\"({self.customer_id}, {self.user_id} ,{self.currency_in_id}, {self.currency_out_id}, {self.currency_in_count}::money)")
                    self.msg.append("Deal created")
                byn_data = dict(conn.execute(f"select * from \"Currency\" where \"id\" = 1;").fetchone())
                self.daily_currency_rate_view.update({byn_data["code"]: byn_data})
                [
                    self.daily_currency_rate_view.update({d.code: dict(d)})
                    for d in conn.execute("select * from \"daily_currency_rate_view\"").fetchall()
                ]
                self.customer_data = dict(
                    conn.execute(f"select * from \"Customer\" where \"id\" = '{self.customer_id}' ;").fetchone()
                )
        except Exception:
            self.errors.append("Something went wrong")
