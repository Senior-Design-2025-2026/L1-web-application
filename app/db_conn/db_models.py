from sqlalchemy import Integer, String, Float, TIMESTAMP, UniqueConstraint, Index, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import Optional

class Base(DeclarativeBase):
    pass

class TemperatureReading(Base):
    __tablename__ = "temperature_readings"

    sensor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped = mapped_column(TIMESTAMP, default=func.now())
    temperature_c: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return f"<TemperatureReading {self.sensor_id}>"

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    phone_num: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email_addr: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        Index("idx_user_id", "user_id"),
    )

    def __repr__(self):
        return f"<User {self.name}>"