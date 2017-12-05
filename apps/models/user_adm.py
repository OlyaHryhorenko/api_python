#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from conf import Conf
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event

Base = declarative_base()
App_Root = os.path.abspath(
    os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), os.pardir))
dbfile = os.path.join(App_Root, Conf("SqLite").read_sqlite())
db_engine = create_engine("sqlite:///{}".format(dbfile), echo=True)
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)

class UserCheck(Base):
    __tablename__ = 'sys_seo_user'
    STATUS_INITIAL_DELFAG = 0
    id = Column(Integer, primary_key=True)
    user_ = Column(String(), unique=True)
    passw_ = Column(String(), nullable=False)
    Delflag = Column(Integer(), default=STATUS_INITIAL_DELFAG)

    def __init__(self, user, passw):
        self.Delflag = 0
        self.user_ = user
        self.passw_ = passw

    #def __repr__(self):
    #    return "TABLE: {0} VALUE [{1},{2},{3}]".format(self.__tablename__,
    #                                                   self.user_,
    #                                                   self.passw_)

class Work_UserCheck(object):
    def __init__(self):
        self.cls = UserCheck

    def get_all(self):
        session = Session()
        print self.cls
        users = session.query(self.cls).order_by(self.cls.id)
        for u in users:
            print u.id, ' ', u.user_, ' ', u.passw_
#new_user = UserCheck("tre", "tre")
#session.add(new_user)
#session.commit()
#for u in users:
#    print u.id, ' ', u.user_, ' ', u.passw_