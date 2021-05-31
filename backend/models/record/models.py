# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  models.py
@Description    :  
@CreateTime     :  2021/5/31 10:25 下午
------------------------------------
@ModifyTime     :  
"""
from models.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Text
from datetime import datetime


class OperateRecords(Base):
    __tablename__ = "operate_records"
    __table_args__ = ({"comment": "数据操作记录表"})
    record_id = Column(BigInteger(),  index=True, primary_key=True)
    operate_username = Column(String(20), nullable=False, index=True, comment="操作的用户")
    operate_time = Column(DateTime(), default=datetime.now, comment="操作的时间")
    operate_ip = Column(String(20), nullable=False, comment="操作的IP")
    operate_type = Column(String(10), nullable=False, comment="操作类型")
    operate_object = Column(String(30), nullable=False, comment="操作的对象")
    operate_detail = Column(Text, comment="操作的具体信息")
