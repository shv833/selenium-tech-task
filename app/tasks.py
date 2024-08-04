from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from .celery_config import app
from .db import SessionLocal, User
import json


def with_webdriver(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        try:
            result = func(driver, *args, **kwargs)
        finally:
            driver.quit()
        return result

    return wrapper


@app.task
@with_webdriver
def fetch_users(driver):
    driver.get("https://jsonplaceholder.typicode.com/users")
    pre_element = driver.find_element(By.TAG_NAME, "pre")
    users = json.loads(pre_element.text)

    print(users)
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
    driver.get("https://random-data-api.com/api/v2/addresses")
    address = json.loads(driver.find_element(By.TAG_NAME, "pre").text)

    driver.get("https://random-data-api.com/api/v2/credit_cards")
    credit_card = json.loads(driver.find_element(By.TAG_NAME, "pre").text)

    db = SessionLocal()
    user = db.query(User).order_by(User.id.desc()).first()
    if user:
        user.address = address
        user.credit_card = credit_card
        db.commit()
    db.close()
