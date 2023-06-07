from sqlalchemy import Column, Numeric, String, Table, Integer, Date, Time

from exchange.datasource import metadata

deal_data_view = Table(
    "deal_data_view",
    metadata,
    Column("deal_id", Integer, nullable=False),
    Column("deal_date", Date, nullable=False),
    Column("deal_time", Time, nullable=False),
    Column("customer_id", Integer, nullable=False),
    Column("customer_first_name", String, nullable=False),
    Column("customer_last_name", String, nullable=False),
    Column("teller_id", Integer, nullable=False),
    Column("teller_first_name", String, nullable=False),
    Column("teller_last_name", String, nullable=False),
    Column("currency_out_code", String, nullable=False),
    Column("currency_in_count", Numeric, nullable=False),
    Column("currency_out_rate_in", Numeric, nullable=False),
    Column("currency_in_code", String, nullable=False),
    Column("currency_out_count", Numeric, nullable=False),
    Column("currency_in_rate_out", Numeric, nullable=False),
)
