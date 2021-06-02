# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  story.py
@Description    :
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""

from fastapi import APIRouter

import core
from db import models

stories = APIRouter(tags=["需求相关"])


@stories.post("/story", name="需求新增")
async def create(story: models.StoryIn_Pydantic):
    """
    环境新增数据库配置目前只提供mysql，需按照如下字典配置
    Args:
        story:

    Returns:

    """
    try:
        story_obj = await models.Story.create(**story.dict(exclude_unset=True))
        return core.Success(data=await models.Story_Pydantic.from_tortoise_orm(story_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@stories.delete("/story/{e_id}", name="需求删除")
async def delete(e_id: int):
    todo_obj = await models.Story.filter(id=e_id).delete()
    if todo_obj:
        return core.Success()
    return core.Fail(message="需求不存在.")


@stories.get("/story", name="查询所有需求")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Story_Pydantic.from_queryset(models.Story.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Story.all().count(), "items": data})


@stories.get("/search/{e_name}", name="查询需求")
async def select_name(e_name: str):
    try:
        data = await models.Story_Pydantic.from_queryset_single(models.Story.get(name=e_name))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@stories.get("/story/{e_id}", name="需求详情")
async def select(e_id: int):
    try:
        data = await models.Story_Pydantic.from_queryset_single(models.Story.get(id=e_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看详情失败.{e}")


@stories.put("/story/{e_id}", name="需求编辑")
async def update(e_id: int, story: models.StoryIn_Pydantic):
    try:
        await models.Story.filter(id=e_id).update(**story.dict(exclude_unset=True))
        return core.Success(data=await models.Story_Pydantic.from_queryset_single(models.Story.get(id=e_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
