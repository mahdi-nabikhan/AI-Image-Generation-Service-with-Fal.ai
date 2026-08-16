from sqlalchemy import Column, Float, Integer
from core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,autoincrement=True,)

    balance_ai = Column(Float,nullable=False,default=1000.0)