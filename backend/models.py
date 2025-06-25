from sqlalchemy import Table, Column, Integer, String, Float, Boolean, ForeignKey
from database import metadata

cats = Table(
    "cats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("years_of_experience", Integer, nullable=False),
    Column("breed", String, nullable=False),
    Column("salary", Float, nullable=False),
)

missions = Table(
    "missions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("cat_id", Integer, ForeignKey("cats.id"), nullable=True),
    Column("completed", Boolean, default=False),
)

targets = Table(
    "targets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("mission_id", Integer, ForeignKey("missions.id")),
    Column("name", String, nullable=False),
    Column("country", String, nullable=False),
    Column("notes", String, default=""),
    Column("completed", Boolean, default=False),
)
