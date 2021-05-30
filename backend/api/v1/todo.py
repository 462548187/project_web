# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  todo.py
@Description    :
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""


from fastapi import APIRouter

import core
from db import models

todos = APIRouter(tags=["代办相关"])


@todos.post("/todo", name="代办新增")
async def create(todo: models.TodoIn_Pydantic):
    """
    环境新增数据库配置目前只提供mysql，需按照如下字典配置
    Args:
        todo:

    Returns:

    """
    try:
        todo_obj = await models.Todo.create(**todo.dict(exclude_unset=True))
        return core.Success(data=await models.Env_Pydantic.from_tortoise_orm(todo_obj))
    except Exception as e:
        return core.Fail(message=f"创建失败.{e}")


@todos.delete("/todo/{e_id}", name="代办删除")
async def delete(e_id: int):
    todo_obj = await models.Todo.filter(id=e_id).delete()
    if todo_obj:
        return core.Success()
    return core.Fail(message="环境不存在.")


@todos.get("/todo", name="查询所有代办")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Todo_Pydantic.from_queryset(models.Todo.all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Todo.all().count(), "items": data})


@todos.get("/todo/{e_id}", name="代办详情")
async def select(e_id: int):
    try:
        data = await models.Todo_Pydantic.from_queryset_single(models.Todo.get(id=e_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"查看详情失败.{e}")


@todos.put("/todo/{e_id}", name="代办编辑")
async def update(e_id: int, todo: models.TodoIn_Pydantic):
    try:
        await models.Todo.filter(id=e_id).update(**todo.dict(exclude_unset=True))
        return core.Success(data=await models.Todo_Pydantic.from_queryset_single(models.Todo.get(id=e_id)))
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")
