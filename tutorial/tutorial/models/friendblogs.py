from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,   
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base

class FriendBlogs(Base):
    __tablename__  = 'friendblogs'
    id = Column(Integer,primary_key = True)
    friend_id = Column(Integer)
    friend_name = Column(Text)
    my_id = Column(Integer, nullable=False)
    blog = Column(Text,nullable = False)