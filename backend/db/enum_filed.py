# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  enum_filed.py
@Description    :  枚举类字符串
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""
from enum import Enum


class Methods(str, Enum):
    """请求方法类型"""
    POST = 'post'
    DELETE = 'delete'
    GET = 'get'
    PUT = 'put'


# https://www.runoob.com/http/http-content-type.html
class ContentType(str, Enum):
    """请求参数类型"""
    PARAMS = 'params'
    DATA = 'data'
    JSON = 'json'


class Standard(str, Enum):
    """接口规范"""
    RESTFUL = 'restful'
    GRAPHQL = 'graphql'


class StoryType(str, Enum):
    Demand = '需求'
    Optimization = '优化'
    Bug = '缺陷'
    Other = '其他'


class PriorityType(str, Enum):
    Urgent = '紧急'
    High = '高'
    Middle = '中'
    Low = '低'
    insignificant = '无关紧要'
    Default = '空'


class ReceiveType(str, Enum):
    Dingding = '钉钉'
    Email = '邮件'
    Weixin = '微信'
