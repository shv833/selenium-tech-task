from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from .celery_config import app
from .db import SessionLocal, User
import json
import logging
import os


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def script(URL, KEY, HOST):
    return """
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "%s", false);
    xhr.setRequestHeader("x-rapidapi-key", "%s");
    xhr.setRequestHeader("x-rapidapi-host", "%s");
    xhr.send(null);
    return xhr.responseText;
    """ % (
        URL,
        KEY,
        HOST,
    )


def with_webdriver(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")

        hub_url = "http://chrome:4444/wd/hub"
        driver = webdriver.Remote(command_executor=hub_url, options=options)

        try:
            result = func(driver, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            raise
        finally:
            try:
                driver.quit()
            except Exception as quit_exception:
                logger.error(f"Failed to quit driver: {quit_exception}")

        return result

    return wrapper


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
    address_script = script(address_url, KEY, HOST)

    address_result = driver.execute_script(address_script)
    address = json.loads(address_result)

    credit_url = (
        "https://fake-information-generator.p.rapidapi.com/fake/credit-card-number"
    )
    credit_script = script(credit_url, KEY, HOST)

    credit_result = driver.execute_script(credit_script)
    credit_card = json.loads(credit_result)

    logger.info(address)
    logger.info(credit_card)

    db = SessionLocal()
    users = db.query(User).order_by(User.id.desc())
    for user in users:
        user.address = address["fake_address"]
        user.credit_card = credit_card["fake_credit_card_number"]
        db.commit()
    db.close()
