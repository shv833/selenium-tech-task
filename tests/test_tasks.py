import pytest
from app.tasks import fetch_users, fetch_address_credit_card
from app.db import User, CreditInfo


@pytest.mark.usefixtures("celery_app_configured")
def test_fetch_users(db_session, subtests):
    result = fetch_users.apply_async()
    result.get(timeout=10)

    users = db_session.query(User).all()

    with subtests.test("Check if users are fetched"):
        assert len(users) > 0


@pytest.mark.usefixtures("celery_app_configured")
def test_fetch_address_credit_card(db_session, subtests):
    result = fetch_address_credit_card.apply_async()
    result.get(timeout=10)

    credit_infos = db_session.query(CreditInfo).all()
    user_count = db_session.query(User).count()

    with subtests.test("Check if credit infos are fetched"):
        assert len(credit_infos) == user_count // 2

    for credit_info in credit_infos:
        with subtests.test("Check if credit info's address is not None"):
            assert credit_info.address is not None

        with subtests.test("Check if credit info's credit card is not None"):
            assert credit_info.credit_card is not None
