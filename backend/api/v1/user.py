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


@user_router.delete("/user/{e_id}", name="用户删除")
async def delete(e_id: int):
    story_obj = await models.User.filter(id=e_id).delete()
    if story_obj:
        return core.Success()
    return core.Fail(message="用户不存在.")


@user_router.get("/user", name="查询所有用户")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.User_Pydantic.from_queryset(models.User.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.User.all().count(), "items": data})


@user_router.get("/search/{user_name}", name="模糊查询用户名称")
async def select_story(user_name: str, limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    try:
        data = await models.User_Pydantic.from_queryset(
            models.User.filter(name__contains=user_name).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@user_router.get("/user/{e_id}", name="用户详情")
async def select(e_id: int):
    try:
        data = await models.User_Pydantic.from_queryset_single(models.User.get(id=e_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看详情失败.{e}")


@user_router.put("/user/{e_id}", name="用户编辑")
async def update(e_id: int, user: models.UserIn_Pydantic):
    try:
        await models.User.filter(id=e_id).update(**user.dict(exclude_unset=True))
        return core.Success(data=await models.User_Pydantic.from_queryset_single(models.User.get(id=e_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
