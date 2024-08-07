from selenium.webdriver.common.by import By
from .celery_config import app
from .db import SessionLocal, User, CreditInfo
from .utils import get_api_info_script, with_webdriver
import json
import os


@app.task
@with_webdriver
def fetch_users(driver):
    driver.get("https://jsonplaceholder.typicode.com/users")
    pre_element = driver.find_element(By.TAG_NAME, "pre")
    users = json.loads(pre_element.text)

    db = SessionLocal()
    for user in users:
        db_user = db.query(User).filter(User.id == user["id"]).first()
        if not db_user:
            db_user = User(
                id=user["id"],
                name=user["name"],
                username=user["username"],
                email=user["email"],
            )
            db.add(db_user)
    db.commit()
    db.close()


@app.task
@with_webdriver
def fetch_address_credit_card(driver):
    KEY = os.environ.get("x-rapidapi-key")
    HOST = os.environ.get("x-rapidapi-host")

    driver.get("data:text/html,<html></html>")

    address_url = "https://fake-information-generator.p.rapidapi.com/fake/address"
    address_script = get_api_info_script(address_url, KEY, HOST)

    address_result = driver.execute_script(address_script)
    address = json.loads(address_result)

    credit_url = (
        "https://fake-information-generator.p.rapidapi.com/fake/credit-card-number"
    )
    credit_script = get_api_info_script(credit_url, KEY, HOST)

    credit_result = driver.execute_script(credit_script)
    credit_card = json.loads(credit_result)

    db = SessionLocal()
    for user in db.query(User).all():
        db_credit_info = (
            db.query(CreditInfo).filter(CreditInfo.user_id == user.id).first()
        )
        if not db_credit_info:
            db_credit_info = CreditInfo(
                user_id=user.id,
                address=address["fake_address"],
                credit_card=credit_card["fake_credit_card_number"],
            )
            db.add(db_credit_info)
        else:
            db_credit_info.address = address["fake_address"]
            db_credit_info.credit_card = credit_card["fake_credit_card_number"]
    db.commit()
    db.close()
