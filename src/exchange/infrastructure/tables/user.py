from sqlalchemy import Boolean, Column, Integer, String, Table, UniqueConstraint, ForeignKey

from exchange.datasource import metadata

user_table = Table(
    "User",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("has_salary_increase", Boolean, nullable=False),
    Column("password", String, nullable=False),
    Column("role_id", Integer, ForeignKey("Role.id"), nullable=False, index=True),
    Column("level_id", Integer, ForeignKey("Salary.level"), nullable=False, index=True),
    Column("active", Boolean, nullable=False),
    UniqueConstraint("email", name="unique_user_email"),
)
