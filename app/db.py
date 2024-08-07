from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os
import time


DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


def create_session():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


engine, SessionLocal = create_session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    credit_info = relationship("CreditInfo", back_populates="user", uselist=False)


class CreditInfo(Base):
    __tablename__ = "creditinfo"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    credit_card = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="credit_info")


def wait_for_db_connection(engine, retries=5, delay=2):
    for i in range(retries):
        try:
            connection = engine.connect()
            connection.close()
            return True
        except Exception as e:
            time.sleep(delay)
    return False


def create_tables():
    if wait_for_db_connection(engine):
        Base.metadata.create_all(bind=engine)
    else:
        print("Could not create tables due to unsuccessful database connection.")


if __name__ == "__main__":
    create_tables()
