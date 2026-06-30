from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # logs SQL (great for demo/debug)
)

SessionLocal = sessionmaker(bind=engine)