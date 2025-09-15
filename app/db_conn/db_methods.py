import pandas as pd

from db_conn.db_models import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine

class DBConnection:
    def __init__(self, db_path):
        self.loc = db_path
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)

    def get_readings(self) -> pd.DataFrame:
        with Session(self.engine) as session:
            readings = session.query(TemperatureReading).all()
        return readings

    def get_readings_by_id(self, id: int) -> pd.DataFrame:
        with Session(self.engine) as session:
            readings = session.query(TemperatureReading).filter(TemperatureReading.sensor_id == id).all()
        return readings

    def get_users(self) -> pd.DataFrame:
        with Session(self.engine) as session:
            users = session.query(User).all()
        return users

    def get_user_by_name(self, name: str) -> pd.DataFrame:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.name == name).all()
        return user

    def create_user(self, name: str, phone_num: str = None, email_addr: str = None):
        with Session(self.engine) as session:
            new_user = User(
                name=name, 
                phone_num=phone_num, 
                email_addr=email_addr
            )
            session.add(new_user)
            try:
                session.commit()
                return new_user
            except IntegrityError:
                session.rollback()
                print(f"User with name '{name}' already exists.")
                return None

    def update_name(self, user_id: int, new_name: str):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.name = new_name
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    print(f"Name '{new_name}' already exists for another user.")

    def update_phone_num(self, user_id: int, new_phone_num: str):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.phone_num = new_phone_num
                session.commit()

    def update_email_addr(self, user_id: int, new_email_addr: str):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.email_addr = new_email_addr
                session.commit()