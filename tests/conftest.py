import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, User, CreditInfo
import os
from app.celery_config import app as celery_app


DB_USER = os.environ.get("TEST_DB_USER")
DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
DB_NAME = os.environ.get("TEST_DB_NAME")
DB_HOST = os.environ.get("TEST_DB_HOST")
DB_PORT = os.environ.get("TEST_DB_PORT")
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def db_session(session):
    yield session
    session.rollback()


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "memory://",
        "result_backend": "cache+memory://",
        "task_always_eager": True,
        "task_eager_propagates": True,
    }


@pytest.fixture(scope="session")
def celery_app_configured(celery_config):
    celery_app.conf.update(celery_config)
    return celery_app
