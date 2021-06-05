# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  push.py
@Description    :  
@CreateTime     :  2021/6/3 12:49 上午
------------------------------------
@ModifyTime     :  
"""

from fastapi import APIRouter

import core
from db import models

push_router = APIRouter(tags=["推送"])


@push_router.post("/push", name="推送新增")
async def create(push: models.PushIn_Pydantic):
    """
    环境新增数据库配置目前只提供mysql，需按照如下字典配置
    Args:
        push:
    Returns:
    """
    try:
        push_obj = await models.Push.create(**push.dict(exclude_unset=True))
        return core.Success(data=await models.Push_Pydantic.from_tortoise_orm(push_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@push_router.delete("/push/{e_id}", name="推送删除")
async def delete(e_id: int):
    push_obj = await models.Push.filter(id=e_id).delete()
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


@push_router.put("/push/{e_id}", name="推送编辑")
async def update(e_id: int, push: models.PushIn_Pydantic):
    try:
        await models.Push.filter(id=e_id).update(**push.dict(exclude_unset=True))
        return core.Success(data=await models.Push_Pydantic.from_queryset_single(models.Push.get(id=e_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
