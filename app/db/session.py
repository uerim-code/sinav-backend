from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings

_url = settings.DATABASE_URL
_sqlite = _url.startswith("sqlite")
_pgbouncer = "pgbouncer=true" in _url

if _sqlite:
    engine = create_engine(_url, echo=settings.ENVIRONMENT == "development")
elif _pgbouncer:
    engine = create_engine(
        _url,
        poolclass=NullPool,
        echo=settings.ENVIRONMENT == "development",
    )
else:
    engine = create_engine(
        _url,
        pool_size=10,
        max_overflow=20,
        pool_recycle=300,
        pool_pre_ping=True,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency — her request icin ayri session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
