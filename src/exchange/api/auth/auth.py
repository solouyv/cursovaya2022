from typing import Any
from typing import Optional

from fastapi import Request
from dependency_injector.wiring import Provide, inject

from exchange.containers import Application
from exchange.datasource import Database


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.user_dict: Optional[dict[str, Any]] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not self.is_valid_password():
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False

    @inject
    def is_valid_password(
        self,
        db: Database = Provide[Application.datasources.postgres]
    ):
        with db.connection() as conn:
            res = conn.execute(f"SELECT * FROM \"user_view_with_roles\" WHERE email = '{self.username}'").fetchone()
        if res.password == self.password:
            self.user_dict = dict(res)
            return True
        return False
