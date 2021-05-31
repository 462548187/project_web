# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  apis.py
@Description    :  
@CreateTime     :  2021/5/31 10:07 下午
------------------------------------
@ModifyTime     :  
"""
from fastapi import APIRouter
from apis.login.controller import login_router
from apis.users.controller import user_router
api_router = APIRouter()
# router注册
api_router.include_router(login_router, tags=["login"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
