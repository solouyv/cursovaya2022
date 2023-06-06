from sqlalchemy import Column, Numeric, Integer, Table

from exchange.datasource import metadata

salaries_view = Table(
    "salaries_view",
    metadata,
    Column("level", Integer, nullable=False),
    Column("salary", Numeric, nullable=False),
    Column("salary_increase", Integer, nullable=False),
)
