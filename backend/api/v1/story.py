# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  story.py
@Description    :  需求路由
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""

from fastapi import APIRouter

import core
from db import models

story_router = APIRouter(tags=["需求相关"])


@story_router.post("/story/{story_id}", name="需求新增和编辑")
async def create(story_id: int, story: models.StoryIn_Pydantic):
    """
    - 新增和编辑需求的接口\n
    - story_id: 需求ID
    """
    try:
        # 判断需求是否被删除
        data = await models.Story.filter(id=story_id, deleted=1)
        if data:
            return core.Fail(message="需求已被删除.")
        # 创建或更新需求
        else:
            # 判断需求是否存在，存在就编辑，不存在就新增
            if await models.Story.filter(id=story_id):
                await models.Story.filter(id=story_id).update(**story.dict(exclude_unset=True))
                return core.Success(data=await models.Story_Pydantic.from_queryset_single(models.Story.get(id=story_id)))
            else:
                try:
                    story_obj = await models.Story.create(**story.dict(exclude_unset=True))
                    return core.Success(data=await models.Story_Pydantic.from_tortoise_orm(story_obj))
                except Exception as e:
                    return core.Fail(message=f"创建失败.{e}")

    except Exception as e:
        return core.Fail(message="需求已存在.")


@story_router.delete("/story/{story_id}", name="需求删除")
async def delete(story_id: int):
    """
    - 删除需求的接口\n
    - story_id: 需求ID
    """
    try:
        # 判断需求是否存在
        await models.Story.get(id=story_id)
        # 判断需求是否被删除
        is_deleted = await models.Story.filter(id=story_id, deleted=1)
        if is_deleted:
            return core.Fail(message="需求已被删除.")
        # 更新需求是否删除为1
        await models.Story.filter(id=story_id).update(deleted=1)
        return core.Success()
    except Exception as e:
        return core.Fail(message="需求不存在.")


@story_router.get("/story/getAll", name="获取所有需求")
async def select_all(limit: int = 10, page: int = 1):
    """
    - 获得所有需求接口\n
    - limit： 每页条数\n
    - int： 当前页面
    """
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    try:
        data = await models.Story_Pydantic.from_queryset(models.Story.filter(deleted=0).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data={"total": await models.Story.all().count(), "items": data})
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@story_router.get("/search/{story_name}", name="模糊查询")
async def select_story(story_name: str, limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    try:
        data = await models.Story_Pydantic.from_queryset(models.Story.filter(name__contains=story_name, deleted=0).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@story_router.get("/story/{story_id}", name="需求详情")
async def select(story_id: int):
    """
    - 获取指定需求ID详情接口\n
    - story_id: 需求ID
    """
    try:
        # 获取指定需求
        # 判断需求是否存在
        await models.Story.get(id=story_id)
        # 判断需求是否被删除
        is_deleted = await models.Story.filter(id=story_id, deleted=1)
        if is_deleted:
            return core.Fail(message="需求已被删除.")
        data = await models.Story_Pydantic.from_queryset_single(models.Story.get(id=story_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"需求不存在.")
