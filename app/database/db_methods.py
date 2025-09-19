from sqlalchemy import create_engine, func, select, update, delete, insert
from sqlalchemy.orm import Session, sessionmaker

from .db_orm import User, Temperature
from pathlib import Path


# ============================================================
#                      USER CONFIGURATIONS
# ============================================================
class Users():
    def __init__(self, db_path):
        path = Path.cwd().joinpath(db_path)
        self.engine  = create_engine(f"sqlite:///{path}")
        self.Session = sessionmaker(self.engine)

    def get_all_users(self):
        with self.Session() as session:
            result = session.execute(select(User))
            return result

    def add_user(self, user: User):
        with self.Session() as session:
            session.add(user)
            session.commit()

    def remove_user(self, user_id:str):
        stmt = delete(User).where(User.user_id == user_id)

        with self.Session() as session:
            session.execute(stmt)
            session.commit()

    def update_name(self, user_id:str, name:str):
        stmt = update(User).where(User.user_id == user_id).values(name = name)

        with self.Session() as session:
            session.execute(stmt)
            session.commit()

    def update_phone_num(self, user_id:int, phone_addr:str):
        stmt = update(User).where(User.user_id == user_id).values(phone_addr = phone_addr)

        with self.Session() as session:
            session.execute(stmt)
            session.commit()

    def update_email_addr(self, user_id:int, email_addr:str):
        stmt = update(User).where(User.user_id == user_id).values(email_addr = email_addr)

        with self.Session() as session:
            session.execute(stmt)
            session.commit()

# ============================================================
#                   TEMPERATURE READINGS
# ============================================================
class Readings():
    def __init__(self, db_path):
        path = Path.cwd().joinpath(db_path)
        self.engine  = create_engine(f"sqlite:///{path}")
        self.Session = sessionmaker(self.engine)

    def get_all_temperatures(self):
        with self.Session() as session:
            return session.execute(
                select(Temperature)
            )

    def add_reading(self, reading: Temperature):
        with self.Session() as session:
            session.add(Temperature)
            session.commit()