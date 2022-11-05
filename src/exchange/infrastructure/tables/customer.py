from sqlalchemy import Column, Integer, String, Table, UniqueConstraint

from exchange.datasource import metadata

customer_table = Table(
    "Customer",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("passport_id", String, nullable=False),
    Column("bank_card_id", String, nullable=True),
    UniqueConstraint("first_name", "last_name", "passport_id", name="unique_customer"),
)
