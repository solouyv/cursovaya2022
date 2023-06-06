from sqlalchemy import Column, String, Table

from exchange.datasource import metadata

card_ids_view = Table(
    "card_ids_view",
    metadata,
    Column("bank_card_id", String, nullable=False),
)
