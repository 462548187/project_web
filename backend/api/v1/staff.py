# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  staff.py
@Description    :  员工路由
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""

from fastapi import APIRouter, Depends

import core
from db import models

staff_router = APIRouter(tags=["员工相关"])


@staff_router.post("/staff", name="新增员工")
async def create(staff: models.StaffIn_Pydantic):
    try:
        staff_obj = await models.Staff.create(**staff.dict(exclude_unset=True))
        return core.Success(data=await models.Staff_Pydantic.from_tortoise_orm(staff_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@staff_router.delete("/staff/{staff_id}", name="员工删除")
async def delete(staff_id: int):
    story_obj = await models.Staff.filter(id=staff_id).delete()
    if story_obj:
        return core.Success()
    return core.Fail(message="员工不存在.")


@staff_router.get("/staff", name="查询所有员工")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Staff_Pydantic.from_queryset(models.Staff.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Staff.all().count(), "items": data})


@staff_router.get("/search/{staff_name}", name="模糊查询")
async def select_story(staff_name: str, limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    try:
        data = await models.Staff_Pydantic.from_queryset(
            models.Staff.filter(name__contains=staff_name).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@staff_router.put("/staff/{staff_id}", name="员工编辑")
async def update(staff_id: int, staff: models.StaffIn_Pydantic):
    try:
        await models.Staff.filter(id=staff_id).update(**staff.dict(exclude_unset=True))
        return core.Success(data=await models.Staff_Pydantic.from_queryset_single(models.Staff.get(id=staff_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
