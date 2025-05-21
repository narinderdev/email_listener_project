# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os

# DATABASE_URL = os.getenv('DB_URL')
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# load_dotenv()  # load .env file

# DATABASE_URL = os.getenv('DB_URL')

# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATABASE_URL = os.getenv('DB_URL')
if not DATABASE_URL:
    raise ValueError("No DB_URL environment variable set")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
