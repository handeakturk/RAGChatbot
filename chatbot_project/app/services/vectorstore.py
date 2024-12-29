from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
from datetime import datetime
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# Çevresel değişkenlerden veritabanı bağlantı bilgilerini al
DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
SERVER = os.getenv("DB_SERVER", "localhost")
DATABASE = os.getenv("DB_DATABASE", "master")
TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "Yes")

# MSSQL bağlantısı için connection string oluştur
connection_string = (
    f"Driver={{{DRIVER}}};"
    f"Server={SERVER};"
    f"Database={DATABASE};"
    f"Trusted_Connection={TRUSTED_CONNECTION};"
)

connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)
engine = create_engine(connection_url)

Base = declarative_base()

# Logs tablosu modeli
class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(String, nullable=False)
    response = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    log_level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    query_data = Column(String, nullable=True)
    alembic = Column(Integer, nullable=True)

# Tabloyu oluştur
Base.metadata.create_all(engine)

# Session oluştur
Session = sessionmaker(bind=engine)
session = Session()
