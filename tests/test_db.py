from app.db import User, CreditInfo


def test_user_creation(db_session):
    new_user = User(name="John Doe", username="johndoe", email="john@example.com")
    db_session.add(new_user)
    db_session.commit()

    user = db_session.query(User).filter_by(username="johndoe").first()
    assert user is not None
    assert user.name == "John Doe"


def test_credit_info_creation(db_session):
    user = User(name="Jane Doe", username="janedoe", email="jane@example.com")
    db_session.add(user)
    db_session.commit()

    new_credit_info = CreditInfo(
        address="123 Main St", credit_card="1234567812345678", user_id=user.id
    )
    db_session.add(new_credit_info)
    db_session.commit()

    credit_info = db_session.query(CreditInfo).filter_by(user_id=user.id).first()
    assert credit_info is not None
    assert credit_info.address == "123 Main St"
