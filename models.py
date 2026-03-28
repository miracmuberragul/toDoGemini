#veritabanında tutacağımız tabloları oluşturacağız
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Todo(Base):#bu sınıf aynı zamanda benim sql tablolarımı oluşturmakta sorumlu olacak
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))#user tablosuyla todolar arasındaki ilişkiyi kurmak için
'''
bu ikisi arasında one to many ilişki var bir userın birçok todosu olabilir
'''
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)#bir email bir kere kaydolabilsin
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String) #kullanıcı,admin vs.
    phone_number = Column(String)

