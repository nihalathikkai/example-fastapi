from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

print("file: database")

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Connect to an existing database with psycopg2 for raw sequel operations

# import psycopg2
# from psycopg2.extras import RealDictCursor
# from time import sleep


# while True:
#     try:
#         conn = psycopg2.connect(dbname={settings.database_db_name}, user={settings.database_username}, password="superuser", host={settings.database_password}, port={settings.database_port}, cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("database connection failed")
#         print("Error: ", error)
#         sleep(2)
