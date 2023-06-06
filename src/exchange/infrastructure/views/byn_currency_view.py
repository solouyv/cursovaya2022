from sqlalchemy import Column, Date, Integer, Numeric, String, Table

from exchange.datasource import metadata

byn_currency_view = Table(
    "byn_currency_view",
    metadata,
    Column("id", Integer, nullable=False),
    Column("code", String, nullable=False),
    Column("rate_in", Numeric, nullable=False),
    Column("rate_out", Numeric, nullable=False),
    Column("data", Date, nullable=False),
)
