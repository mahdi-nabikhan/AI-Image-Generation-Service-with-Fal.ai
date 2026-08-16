from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import setting


engine = create_engine(
    setting.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Provide a SQLAlchemy database session for FastAPI dependencies.

    The session is created for each request and guaranteed to be closed
    after the request completes, including when an exception occurs.

    Yields:
        Session: An active SQLAlchemy database session.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)