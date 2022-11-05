from sqlalchemy import Column, Numeric, String, Table

from exchange.datasource import metadata

daily_cash_amount = Table(
    "daily_cash_amount",
    metadata,
    Column("code", String, nullable=False),
    Column("amount", Numeric, nullable=False),
)
