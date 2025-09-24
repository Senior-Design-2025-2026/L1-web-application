from sqlalchemy import create_engine, func, Integer, String, Time, Float, UniqueConstraint
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import Optional

# ================================================== SQL ALCHEMY ================================================== 
# this is a super easy to use python package for handling transactional database connections agnostically using OOP
# docs: https://www.sqlalchemy.org/

# ================= BASE  ==================
# this classname doesnt need to be "Base", 
# however, passing DeclarativeBase (via orm)
# creates a Base class which we can extend
# to use SQLAlchemy's ORM functionality.
# Extending Base declares any child class
# as a Database Table with the following:
# __tablename__ : the name of the table
# attributes : fields of the table
#
# This is simply DDL; calling
#     Base.metadata.create_all(engine)
# executes the creation of the tables
#     Base.metadata.drop_all(engine)
# destroys all tables.
# 
# USAGE:
# - run this script directly; do not use
#   DDL at runtime. Instead, use the DML 
#   methods within db_methods.py
class Base(DeclarativeBase):
    pass

class Temperature(Base):
    """A sensor reading within 'temperature_readings'"""
    __tablename__ = "temperature_readings"

    id: Mapped[int]              = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[int]       = mapped_column(Integer, nullable=False)
    timestamp: Mapped[str]       = mapped_column(String, nullable=False)
    temperature_c: Mapped[float] = mapped_column(Float, nullable=True)

    def __repr__(self):
        return f"<temperature_readings(sensor_id={self.sensor_id}, timestamp={self.timestamp}, temperature_c={self.temperature_c})>"

class User(Base):
    """A user's configuration within 'user_configurations'"""
    __tablename__ = "user_configurations"

    user_id: Mapped[int]              = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]                 = mapped_column(String(30), nullable=False)
    phone_num: Mapped[Optional[str]]  = mapped_column(String(15), nullable=True)
    email_addr: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "name"),            
    )

    def __repr__(self):
        return f"<user_configurations(user_id={self.user_id}, name={self.name}, phone_num={self.phone_num}, email_addr={self.email_addr}>"

if __name__ == "__main__":
    print("RUNNING")
    engine = create_engine("sqlite:///sqlite/lab1.db", echo=True)

    tables: list[Base] = [Temperature(), User()]

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    matt = User(
        name="Matt",
        phone_num="6087973815",
        email_addr="mnkrueger@uiowa.edu"
    )

    user1 = User(
        name="user1",
        phone_num="abcdefg",
        email_addr="hello@gmail.com"
    )

    with Session(engine) as session:
        session.add(matt)
        session.add(user1)
        session.commit()