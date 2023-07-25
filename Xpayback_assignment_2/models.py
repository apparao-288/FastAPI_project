from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users_xpayback"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(Integer)
