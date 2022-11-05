from sqlalchemy import Column, Date, DateTime, Integer, Numeric, Table, ForeignKey

from exchange.datasource import metadata

deal_table = Table(
    "Deal",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("customer_id", Integer, ForeignKey("Customer.id"), nullable=False, index=True),
    Column("user_id", Integer, ForeignKey("User.id"), nullable=False, index=True),
    Column("currency_in_id", Integer, ForeignKey("Currency.id"), nullable=False, index=True),
    Column("currency_out_id", Integer, ForeignKey("Currency.id"), nullable=False, index=True),
    Column("currency_in_count", Numeric, nullable=False),
    Column("data", Date, nullable=False),
    Column("time", DateTime, nullable=False),
)
