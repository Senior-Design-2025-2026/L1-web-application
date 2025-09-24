from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session
import pandas as pd
from app.app import celery_app

from .db_orm import User, Temperature
from pathlib import Path

class DB():
    def __init__(self, db_path):
        path         = Path.cwd().joinpath(db_path)
        self.engine  = create_engine(f"sqlite:///{path}")

    def get_all_users(self):
        with self.engine.connect() as conn:
            query = select(User)
            result = pd.read_sql_query(query, con=conn)
            return result

    def add_user(self, user: User):
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def remove_user(self, user_id:str):
        stmt = delete(User).where(User.user_id == user_id)

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def update_name(self, user_id:str, name:str):
        stmt = update(User).where(User.user_id == user_id).values(name = name)

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def update_phone_num(self, user_id:int, phone_addr:str):
        stmt = update(User).where(User.user_id == user_id).values(phone_addr = phone_addr)

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def update_email_addr(self, user_id:int, email_addr:str):
        stmt = update(User).where(User.user_id == user_id).values(email_addr = email_addr)

        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()

    def get_all_temperatures(self):
        with Session(self.engine) as session:
            return session.execute(
                select(Temperature)
            )

    @celery_app.task
    def add_reading(self, sensor_id: str, timestamp):
        with Session(self.engine) as session:
            session.add(Temperature)
            session.commit()