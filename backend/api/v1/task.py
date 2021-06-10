# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  task.py
@Description    :  任务路由
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""
from tortoise.transactions import in_transaction

import core
from fastapi import APIRouter
from db import models

task_router = APIRouter(tags=["任务相关"])


@task_router.post("/task", name="任务新增")
async def create(task: models.TaskInStoryName):
    """
    环境新增数据库配置目前只提供mysql，需按照如下字典配置
    Args:
        task:
    Returns:

    """
    try:
        story_obj = [await models.Staff.get(id=staff) for staff in task.story_name_list]
        dev_obj = [await models.Staff.get(id=staff) for staff in task.story_dev_list]
        tester_obj = [await models.Staff.get(id=staff) for staff in task.story_tester_list]
        del task.story_name_list, task.story_dev_list, task.story_tester_list
        async with in_transaction():
            task_obj = await models.Task.create(**task.dict(exclude_unset=True))
            await task_obj.stroy_name.add(*story_obj)
            await task_obj.dev_name.add(*dev_obj)
            await task_obj.tester_name.add(*tester_obj)

            return core.Success(data=await models.Task_Pydantic.from_tortoise_orm(task_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@task_router.delete("/task/{task_id}", name="任务删除")
async def delete(task_id: int):
    task_obj = await models.Task.filter(id=task_id).delete()
    if task_obj:
        return core.Success()
    return core.Fail(message="任务不存在.")


@task_router.get("/task", name="查询所有任务")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Task_Pydantic.from_queryset(models.Task.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Task.all().count(), "items": data})


@task_router.get("/search/{task_name}", name="模糊查询")
async def select_task(task_name: str, limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    try:
        data = await models.Task_Pydantic.from_queryset(models.Task.filter(name__contains=task_name).all().order_by('-created_at').offset(skip).limit(limit))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看失败.{e}")


@task_router.get("/task/{task_id}", name="任务详情")
async def select(task_id: int):
    try:
        data = await models.Task_Pydantic.from_queryset_single(models.Task.get(id=task_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看详情失败.{e}")


@task_router.put("/task/{task_id}", name="任务编辑")
async def update(task_id: int, task: models.TaskInStoryName):
    try:
        task_obj = await models.Task.get(id=task_id)
        story_obj = [await models.Staff.get(id=staff) for staff in task.story_name_list]
        dev_obj = [await models.Staff.get(id=staff) for staff in task.story_dev_list]
        tester_obj = [await models.Staff.get(id=staff) for staff in task.story_tester_list]
        del task.story_name_list, task.story_dev_list, task.story_tester_list
        async with in_transaction():
            await models.Task.filter(id=task_id).update(**task.dict(exclude_unset=True))
            # 清除该对象与stroy_name的关系
            await task_obj.stroy_name.clear()
            await task_obj.dev_name.clear()
            await task_obj.tester_name.clear()
            # 添加关系
            await task_obj.stroy_name.add(*story_obj)
            await task_obj.dev_name.add(*dev_obj)
            await task_obj.tester_name.add(*tester_obj)
            return core.Success(data=await models.Task_Pydantic.from_queryset_single(models.Task.get(id=task_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
