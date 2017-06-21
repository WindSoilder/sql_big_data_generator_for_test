from sqlalchemy import Column, Integer, String, UniqueConstraint, DateTime, Float
from sqlalchemy.schema import ForeignKey

from ..database import Base, db_session

class ConsumeType(Base):
    __tablename__ = 'consume_type'
    __table_args__ = (UniqueConstraint('user_id', 'name', name='_user_typename_uc'), )

    type_id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    comment = Column(String(500))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    @staticmethod
    def get_consume_type(self, type_id):
        consume_type = db_session.query(self.__class__).\
                       filter(self.__class__.type_id == type_id).first()
        return consume_type

    def update_consume_type(self, **kwargs):
        pass

class ConsumePlan(Base):
    __tablename__ = 'consume_plan'
    __table_args__ = (UniqueConstraint('user_id', 'title', name='_user_title_uc'), )

    plan_id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False)   # may need index
    end_date = Column(DateTime, nullable=False)     # may need index
    money = Column(Float, nullable=False)           # may need index
    title = Column(String(50), nullable=False)
    comment = Column(String(500), nullable=True)

    type_id = Column(Integer, ForeignKey('consume_type.type_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def update_consume_plan(self, **kwargs):
        pass

    @staticmethod
    def get_consume_plan(self, plan_id):
        consume_plan = db_session.query(self.__class__).\
                       filter(self.__class__.plan_id == plan_id).first()
        return consume_plan

class ConsumeItem(Base):
    __tablename__ = 'consume_item'
    __table_args__ = (UniqueConstraint('user_id', 'title', name='_user_title_uc'), )

    item_id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)        # may need index
    money = Column(Float, nullable=False)          # may need index
    title = Column(String(50), nullable=False)
    comment = Column(String(500), nullable=True)
    type_id = Column(Integer, ForeignKey('consume_type.type_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def update_consume_item(self, **kwargs):
        pass

    @staticmethod
    def get_consume_item(self, item_id):
        consume_item = db_session.query(self.__class__).\
                       filter(self.__clsss__.item_id == item_id).first()
        return consume_item
