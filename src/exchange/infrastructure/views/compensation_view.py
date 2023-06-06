from sqlalchemy import Column, Numeric, String, Table, Integer, Date

from exchange.datasource import metadata

compensation_view = Table(
    "compensation_view",
    metadata,
    Column("id", Integer, nullable=False),
    Column("name", String, nullable=False),
    Column("role", String, nullable=False),
    Column("level", Integer, nullable=False),
    Column("salary", Numeric, nullable=False),
    Column("increase", Integer, nullable=False),
    Column("compensation", Numeric, nullable=False),
    Column("date", Date, nullable=False),
)
