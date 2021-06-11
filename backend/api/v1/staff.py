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
from typing import Optional

from fastapi import APIRouter

import core
from db import models

staff_router = APIRouter(tags=["员工相关"])


@staff_router.post("/staff/add/{staff_id}", name="员工新增编辑")
async def add(staff_id: Optional[int], staff: models.StaffIn_Pydantic):
    """
     - 新增和编辑员工的接口\n
     - staff_id: 员工ID
     """
    try:
        # 判断员工是否被删除
        data = await models.Staff.filter(id=staff_id, deleted=1)
        if data:
            return core.Fail(message="员工已被删除.")
        # 创建或更新项目
        else:
            # 判断员工是否存在，存在就编辑，不存在就新增
            if await models.Staff.filter(id=staff_id):
                await models.Staff.filter(id=staff_id).update(**staff.dict(exclude_unset=True))
                return core.Success(data=await models.Staff_Pydantic.from_queryset_single(models.Staff.get(id=staff_id)))
            else:
                try:
                    staff_obj = await models.Staff.create(**staff.dict(exclude_unset=True))
                    return core.Success(data=await models.Staff_Pydantic.from_tortoise_orm(staff_obj))
                except Exception as e:
                    return core.Fail(message=f"创建失败.{e}")

    except Exception as e:
        return core.Fail(message="员工已存在.")


@staff_router.delete("/staff/del/{staff_id}", name="员工删除")
async def delete(staff_id:  Optional[int]):
    """
    - 删除员工的接口\n
    - staff_id: 员工ID
    """
    try:
        # 判断员工是否存在
        await models.Staff.get(id=staff_id)
        # 判断项目是否被删除
        is_deleted = await models.Staff.filter(id=staff_id, deleted=1)
        if is_deleted:
            return core.Fail(message="员工已被删除.")
        # 更新员工是否删除为1
        await models.Staff.filter(id=staff_id).update(deleted=1)
        return core.Success()
    except Exception as e:
        return core.Fail(message="员工不存在.")


@staff_router.get("/staff/getAll", name="查询所有员工")
async def select_all(limit: int = 10, page: int = 1):
    """
    - 获得所有员工接口\n
    - limit： 每页条数\n
    - int： 当前页面
    """
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Staff_Pydantic.from_queryset(models.Staff.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Staff.all().count(), "items": data})


@staff_router.get("/staff/search/{staff_name}", name="模糊查询")
async def select_story(staff_name: str, limit: int = 10, page: int = 1):
    """
    - 获得所有项目接口\n
    - staff_name： 搜索员工姓名
    - limit： 每页条数\n
    - int： 当前页面
    """
    skip = (page - 1) * limit
    try:
        data = await models.Staff_Pydantic.from_queryset(
            models.Staff.filter(name__contains=staff_name).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")
