from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from .db import engine, SessionLocal, User, CreditInfo, Base


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    html_content = """
    <html>
        <head>
            <title>User Information</title>
        </head>
        <body>
            <h1>User Information</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Address</th>
                    <th>Credit Card</th>
                </tr>
    """
    for user in users:
        credit_info = db.query(CreditInfo).filter(CreditInfo.user_id == user.id).first()
        html_content += f"""
                <tr>
                    <td>{user.id}</td>
                    <td>{user.name}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td>{credit_info.address if credit_info else 'N/A'}</td>
                    <td>{credit_info.credit_card if credit_info else 'N/A'}</td>
                </tr>
        """
    html_content += """
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
