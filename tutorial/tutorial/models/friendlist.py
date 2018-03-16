from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,   
    Text,
)
from sqlalchemy.orm import relationship

from .meta import Base

class FriendList(Base):
    __tablename__  = 'friendlist'
    id = Column(Integer,primary_key = True)
    friend_id = Column(Integer)
    my_id = Column(ForeignKey('user.id'), nullable=False)
    my_id_relation = relationship('User',backref= 'User')

