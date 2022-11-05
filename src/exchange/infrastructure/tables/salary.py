from sqlalchemy import Column, Integer, Numeric, Table

from exchange.datasource import metadata

salary_table = Table(
    "Salary",
    metadata,
    Column("level", Integer, primary_key=True, autoincrement=True),
    Column("salary", Numeric, nullable=False),
    Column("salary_increase", Numeric, nullable=False),
)
