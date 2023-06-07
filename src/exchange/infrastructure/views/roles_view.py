from sqlalchemy import Column, Integer, Table, String

from exchange.datasource import metadata

roles_view = Table(
    "roles_view",
    metadata,
    Column("id", Integer, nullable=False),
    Column("name", String, nullable=False),
)
