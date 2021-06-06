# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  push.py
@Description    :  推送路由
@CreateTime     :  2021/6/3 12:49 上午
------------------------------------
@ModifyTime     :  
"""

from fastapi import APIRouter
from tortoise.transactions import in_transaction

import core
from db import models

push_router = APIRouter(tags=["推送"])


@push_router.post("/push", name="推送新增")
async def create(push: models.PushInName):
    """
    环境新增数据库配置目前只提供mysql，需按照如下字典配置
    Args:
        push:
    Returns:
    """
    try:

        push_name_obj = [await models.Staff.get(id=staff) for staff in push.push_name_list]
        del push.push_name_list
        async with in_transaction():
            push_obj = await models.Push.create(**push.dict(exclude_unset=True))
            await push_obj.at_name.add(*push_name_obj)
            return core.Success(data=await models.Push_Pydantic.from_tortoise_orm(push_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@push_router.delete("/push/{push_id}", name="推送删除")
async def delete(push_id: int):
    push_obj = await models.Push.filter(id=push_id).delete()
    if push_obj:
        return core.Success()
    return core.Fail(message="推送不存在.")


@push_router.get("/push", name="查询所有推送")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Push_Pydantic.from_queryset(models.Push.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Push.all().count(), "items": data})


@push_router.get("/search/{push_name}", name="模糊推送需求名称")
async def select_push(push_name: str, limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    try:
        data = await models.Push_Pydantic.from_queryset(models.Push.filter(name__contains=push_name).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@push_router.put("/push/{push_id}", name="推送编辑")
async def update(push_id: int, push: models.PushIn_Pydantic):
    try:
        await models.Push.filter(id=push_id).update(**push.dict(exclude_unset=True))
        return core.Success(data=await models.Push_Pydantic.from_queryset_single(models.Push.get(id=push_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
