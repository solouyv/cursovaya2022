from sqlalchemy import Column, Numeric, String, Table, Float

from exchange.datasource import metadata

monthly_currency_amounts = Table(
    "monthly_currency_amounts",
    metadata,
    Column("bcode", String, nullable=False),
    Column("bought_amount", Float, nullable=False),
    Column("scode", String, nullable=False),
    Column("sold_amount", Float, nullable=False),
)
