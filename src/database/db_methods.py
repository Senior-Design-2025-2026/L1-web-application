from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session
import pandas as pd
from typing import Union
from .db_orm import User, Temperature
from pathlib import Path


class DB:
    def __init__(self, db_path):
        path = Path.cwd().joinpath(db_path)
        self.engine = create_engine(f"sqlite:///{path}")

    def get_all_users(self):
        with self.engine.connect() as conn:
            query = select(User)
            result = pd.read_sql_query(query, con=conn)
            return result

    def add_user(self, name: str, phone_num: Union[str, None], email_addr: Union[str, None]):
        user = User(name=name, phone_num=phone_num, email_addr=email_addr)
        print("ADDING user", user)
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def remove_user(self, user_id: str):
        stmt = delete(User).where(User.user_id == user_id)
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def update_name(self, user_id: str, name: str):
        stmt = update(User).where(User.user_id == user_id).values(name=name)
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def update_phone_num(self, user_id: int, phone_addr: str):
        stmt = update(User).where(User.user_id == user_id).values(phone_addr=phone_addr)
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def update_email_addr(self, user_id: int, email_addr: str):
        stmt = update(User).where(User.user_id == user_id).values(email_addr=email_addr)
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def get_all_temperatures(self):
        with self.engine.connect() as conn:
            query = select(Temperature)
            result = pd.read_sql_query(query, con=conn)
            return result

# TODO celery
# @celery_app.task
def add_reading(sensor_id: str, timestamp, temperature: float):
    print("ADDING RECORD")
    db = DB("app/database/sqlite/lab1.db")
    reading = Temperature(sensor_id=sensor_id, timestamp=timestamp, temperature_c=temperature)
    with Session(db.engine) as session:
        session.add(reading)
        session.commit()