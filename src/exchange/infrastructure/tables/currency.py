from sqlalchemy import Column, Date, Integer, Numeric, String, Table

from exchange.datasource import metadata

currency_table = Table(
    "Currency",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", String, nullable=False),
    Column("data", Date, nullable=False),
    Column("rate_in", Numeric, nullable=False),
    Column("rate_out", Numeric, nullable=False),
)
