from sqlalchemy import Column, String, Table, Integer

from exchange.datasource import metadata

deal_report_view = Table(
    "deal_report_view",
    metadata,
    Column("name", String, nullable=False),
    Column("level", Integer, nullable=False),
    Column("role", String, nullable=False),
    Column("deal_count", Integer, nullable=False),
)
