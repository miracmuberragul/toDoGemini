#veritabanıyla nasıl bağlatı yapacağımızı yazacağız
from sqlalchemy import create_engine #sql tabanlı vetitabanlarıyla çalışırken bağlantı işlemlerini yapmaya yarayan bir kütüphane
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///todoai-app.db" #bu bizim dbmiz uygulamamnın içinde olacak demek

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)#bu db bağlantısını alıp nasıl bağlantı açacağına bakıyor

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#bu db bağlantısını alıp bağlantıyı oluşturuor

Base = declarative_base()