from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# conn. string format: 'postgresql://<username>:<password>@<ip-address/hostname/domain>/<DB_name>'

DATABASE_CONN_STRING = 'postgresql://postgres:password@localhost/fastapi-learn'

engine = create_engine(DATABASE_CONN_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
