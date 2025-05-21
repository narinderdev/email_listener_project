from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv('DB_URL')
if not DATABASE_URL:
    raise ValueError("No DB_URL environment variable set")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base from app.models where ProcessedEmail is declared
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
