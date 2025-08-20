from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from cruxgen.configuration.settings import Config
from sqlalchemy.orm import sessionmaker

settings = Config()

DATABASE_URL = f"postgresql://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}/{settings.POSTGRESQL_DB}"

engine = create_engine(DATABASE_URL)

def test_db_connection():
    """
    Tests the database connection by executing a simple query.
    """
    try:
        # Use a connection context manager to ensure the connection is closed
        with engine.connect() as _:
            # Execute a simple query to test the connection
            return True

    except OperationalError as e:
        return False

def get_database():
    # engine, _ = setup_database(DATABASE_URL)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()