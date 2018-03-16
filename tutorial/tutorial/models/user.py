from sqlalchemy import (Column,Integer,Text,)

from .meta import Base

class User(Base):
    __tablename__  = 'user'
    id = Column(Integer,primary_key = True)
    username = Column(Text,nullable = False ,unique = True)
    password = Column(Text,nullable = False)
    email = Column(Text,nullable = False ,unique = True)
    age = Column(Integer,nullable = False)