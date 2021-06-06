# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  user.py
@Description    :  用户路由
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""

from fastapi import APIRouter, Depends

import core
from db import models

user_router = APIRouter(tags=["用户相关"])


@user_router.get("/info", name="获取当前登录用户信息")
async def info(user: models.UserIn_Pydantic = Depends(core.get_current_user)):
    """
    - token
    :return: 用户除密码外的信息
    """
    return core.Success(data=await models.User_Pydantic.from_tortoise_orm(user))


@user_router.post("/user", name="新增用户")
async def create(user: models.UserIn_Pydantic):
    """
    - name：str
    - username： str
    - password： str
    :return: 用户除密码外的信息
    """
    user.password = core.get_password_hash(user.password)
    user_obj = await models.User.create(**user.dict(exclude_unset=True))
    # from_tortoise_orm 从 数据表中序列化
    return core.Success(data=await models.User_Pydantic.from_tortoise_orm(user_obj))
