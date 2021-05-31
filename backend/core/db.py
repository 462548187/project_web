# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  db.py
@Description    :  
@CreateTime     :  2021/5/31 9:52 下午
------------------------------------
@ModifyTime     :  
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# 创建连接
engine = create_engine(settings.DB_URL, pool_pre_ping=True, pool_recycle=3600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


def get_session():
    return Session()