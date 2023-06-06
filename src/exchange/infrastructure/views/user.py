from sqlalchemy import Column, Integer, String, Table

from exchange.datasource import metadata

user_with_roles_view = Table(
    "user_view_with_roles",
    metadata,
    Column("user_id", Integer),
    Column("user", String, nullable=False),
    Column("password", String, nullable=False),
    Column("email", String, nullable=False),
    Column("role", String, nullable=True),
    Column("level", Integer, nullable=True)
)
