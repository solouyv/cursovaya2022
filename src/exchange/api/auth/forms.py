from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Request
from sqlalchemy import func, select

from exchange.containers import Application
from exchange.datasource import Database
from exchange.infrastructure.views.user import user_with_roles_view


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
    def is_valid_password(self, db: Database = Provide[Application.datasources.postgres]):
        with db.connection() as conn:
            if conn.execute(func.public.check_password(self.username, self.password)).fetchone()[0]:
                self.user_dict = dict(
                    conn.execute(
                        select([user_with_roles_view]).where(user_with_roles_view.c.email == self.username)
                    ).fetchone()
                )
                return True
            return False
