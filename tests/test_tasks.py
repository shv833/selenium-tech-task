import pytest
from app.tasks import fetch_users, fetch_address_credit_card
from app.db import User, CreditInfo


@pytest.mark.usefixtures("celery_app_configured")
def test_fetch_users(db_session):
    result = fetch_users.apply_async()
    result.get(timeout=10)

    users = db_session.query(User).all()
    assert len(users) > 0


@pytest.mark.usefixtures("celery_app_configured")
def test_fetch_address_credit_card(db_session):
    result = fetch_address_credit_card.apply_async()
    result.get(timeout=10)

    credit_infos = db_session.query(CreditInfo).all()
    assert len(credit_infos) > 0
