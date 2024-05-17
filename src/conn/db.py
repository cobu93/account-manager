
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import URL
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT


service_url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME,
        port=DB_PORT
    )

engine = create_engine(service_url, echo=True)

def get_session():
    session = Session(engine)
    
    try:
        yield session
    finally:
        session.close()
    