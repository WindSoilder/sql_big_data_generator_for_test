from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base, db_session

user_channel = Table('user_channel', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.user_id')),
    Column('channel_id', Integer, ForeignKey('channel.channel_id'))
)

class Channel(Base):
    __tablename__ = 'channel'

    channel_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    comment = Column(String(500), nullable=True)
    level = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    users = relationship('User', 
                         secondary=user_channel,
                         back_populates="channels")

    @staticmethod
    def get_channel(channel_id):
        channel = db_session.query(Channel).filter(Channel.channel_id == channel_id).first()
        return channel