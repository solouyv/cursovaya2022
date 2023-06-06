from sqlalchemy import Column, Integer, String, Table

from exchange.datasource import metadata

role_table = Table(
    "Role",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
)
