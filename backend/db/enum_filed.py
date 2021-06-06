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
    demand = '需求',
    optimization = '优化',
    bug = '缺陷',
    others = '其他'
