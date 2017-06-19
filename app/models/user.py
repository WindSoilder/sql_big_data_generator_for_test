from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import ProgrammingError
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import Base, db_session
from .consume import ConsumeType, ConsumePlan, ConsumeItem
from .channel import user_channel, Channel

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    age = Column(Integer)           # may need index
    address = Column(String(100))   # may need index
    job = Column(String(100))       # may need index
    password_hash = Column(String(256), nullable=False)

    channels = relationship('Channel',
                            secondary=user_channel,
                            back_populates='users')

    @staticmethod
    def create_user(name, password, 
                    age=None, address=None, job=None):
        user = User(name=name, password_hash=password,
                    age=age, address=address, job=job)
        try:
            db_session.add(user)
        except ProgrammingError as e:
            db_session.rollback()
        else:
            db_session.commit()
        return user

    @staticmethod
    def get_user(user_id):
        user = db_session.query(User).filter(User.user_id == user_id).first()
        return user

    def create_consume_type(self, type_name, comment=None):
        consume_type = ConsumeType(name=type_name, comment=comment, 
                                   user_id=self.user_id)
        db_session.add(consume_type)
        db_session.commit()

    def create_consume_item(self, date, money, title, type_id, comment=None):
        consume_item = ConsumeItem(date=date, money=money, title=title, 
                                   type_id=type_id, user_id=self.user_id, comment=comment)
        db_session.add(consume_item)
        db_session.commit()

    def create_consume_plan(self, start_date, end_date, money, title, type_id, coment=None):
        consume_plan = ConsumePlan(start_date=start_date, end_date=end_date, money=money,
                                   title=title, type_id=type_id, user_id=self.user_id, comment=comment)
        db_session.add(consume_plan)
        db_session.commit()

    def create_channel(self, name, level, comment=None):
        channel = Channel(name=name, level=level, comment=comment, user_id=self.user_id)
        channel.users.append(self)
        db_session.add(channel)
        db_session.commit()

    def join_channel(self, channel_id):
        channel = db_session.query(Channel).filter(Channel.channel_id == channel_id).first()
        channel.users.append(self)
        db_session.add(channel)
        db_session.commit()

    @property
    def password(self):
        raise ValueError("You can't access the password property directly")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
