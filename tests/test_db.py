from app.db import User, CreditInfo


def test_user_creation(db_session, subtests):
    new_user = User(name="John Doe", username="johndoe", email="john@example.com")
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter_by(username="johndoe").first()

    with subtests.test("Check if user is created"):
        assert user is not None

    with subtests.test("Check user's name"):
        assert user.name == "John Doe"

    with subtests.test("Check user's email"):
        assert user.email == "john@example.com"


def test_credit_info_creation(db_session, subtests):
    user = User(name="Jane Doe", username="janedoe", email="jane@example.com")
    db_session.add(user)
    db_session.commit()

    new_credit_info = CreditInfo(
        address="123 Main St", credit_card="1234567812345678", user_id=user.id
    )
    db_session.add(new_credit_info)
    db_session.commit()

    credit_info = db_session.query(CreditInfo).filter_by(user_id=user.id).first()

    with subtests.test("Check if credit info is created"):
        assert credit_info is not None

    with subtests.test("Check credit info's address"):
        assert credit_info.address == "123 Main St"

    with subtests.test("Check credit info's credit card"):
        assert credit_info.credit_card == "1234567812345678"
