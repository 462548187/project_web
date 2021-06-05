"""
project: apiAutoTestWeb
file: project.py
author: liuyue
date: 2021/4/18
desc: 项目路由
"""
from fastapi import APIRouter
from tortoise.transactions import in_transaction

import core
from db import models

project_router = APIRouter(tags=['项目相关'])


@project_router.post("/project", name="创建项目")
async def create(project: models.ProjectIn_Pydantic):
    """
    :param project: name 字段唯一

    :return:
    """
    try:
        project_obj = await models.Project.create(**project.dict(exclude_unset=True))
        # from_tortoise_orm 从 数据表中序列化， 针对 模型类对象
        return core.Success(data=await models.Project_Pydantic.from_tortoise_orm(project_obj))
    except Exception as e:
        return core.Fail(message="项目已存在.")


@project_router.delete("/project/{p_id}", name="删除项目")
async def delete(p_id: int):
    project_obj = await models.Project.filter(id=p_id).delete()
    if project_obj:
        return core.Success()
    return core.Fail(message="项目不存在.")


# https://tortoise-orm.readthedocs.io/en/latest/CHANGELOG.html?highlight=from_queryset_single#id27
@project_router.get("/project", name="获取所有项目")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Project_Pydantic.from_queryset(models.Project.all().order_by('-created_at').offset(skip).limit(limit))
    # await models.Project.all().count()
    return core.Success(data={"total": await models.Project.all().count(), "items": data})


@project_router.get("/project/{p_id}", name="获取项目详细")
async def select(p_id: int):
    data = await models.Project_Pydantic.from_queryset_single(models.Project.get(id=p_id))
    return core.Success(data=data)


@project_router.put("/project/{p_id}", name="编辑项目")
async def update(p_id: int, project: models.ProjectIn_Pydantic):
    await models.Project.filter(id=p_id).update(**project.dict(exclude_unset=True))
    return core.Success(data=await models.Project_Pydantic.from_queryset_single(models.Project.get(id=p_id)))


@project_router.get("/project_router", name="获取所有项目不分页")
async def get_projects():
    data = await models.Project_Pydantic.from_queryset(models.Project.all())
    return core.Success(data={"total": len(data), "items": data})
