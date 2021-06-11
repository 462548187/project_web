# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  project.py
@Description    :  项目路由
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""
import core
from db import models
from typing import Optional
from fastapi import APIRouter

project_router = APIRouter(tags=['项目相关'])


@project_router.post("/project/add/{project_id}", name="项目新增编辑")
async def update(project_id: Optional[int], project: models.ProjectIn_Pydantic):
    """
    - 新增和编辑项目的接口\n
    - project_id: 项目ID
    """
    try:
        # 判断项目是否被删除
        data = await models.Project.filter(id=project_id, deleted=1)
        if data:
            return core.Fail(message="项目已被删除.")
        # 创建或更新项目
        else:
            # 判断项目是否存在，存在就编辑，不存在就新增
            if await models.Project.filter(id=project_id):
                await models.Project.filter(id=project_id).update(**project.dict(exclude_unset=True))
                return core.Success(data=await models.Project_Pydantic.from_queryset_single(models.Project.get(id=project_id)))
            else:
                try:
                    project_obj = await models.Project.create(**project.dict(exclude_unset=True))
                    return core.Success(data=await models.Project_Pydantic.from_tortoise_orm(project_obj))
                except Exception as e:
                    return core.Fail(message=f"创建失败.{e}")

    except Exception as e:
        return core.Fail(message="项目已存在.")


@project_router.delete("/project/del/{project_id}", name="删除项目")
async def delete(project_id: Optional[int]):
    """
    - 删除项目的接口\n
    - project_id: 项目ID
    """
    try:
        # 判断项目是否存在
        await models.Project.get(id=project_id)
        # 判断项目是否被删除
        is_deleted = await models.Project.filter(id=project_id, deleted=1)
        if is_deleted:
            return core.Fail(message="项目已被删除.")
        # 更新项目是否删除为1
        await models.Project.filter(id=project_id).update(deleted=1)
        return core.Success()
    except Exception as e:
        return core.Fail(message="项目不存在.")


# https://tortoise-orm.readthedocs.io/en/latest/CHANGELOG.html?highlight=from_queryset_single#id27
@project_router.get("/project/getAll", name="获取所有项目")
async def select_all(limit: int = 10, page: int = 1):
    """
    - 获得所有项目接口\n
    - limit： 每页条数\n
    - int： 当前页面
    """
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.Project_Pydantic.from_queryset(models.Project.filter(deleted=0).all().order_by('-created_at').offset(skip).limit(limit))
    return core.Success(data={"total": await models.Project.all().count(), "items": data})


@project_router.get("/project/detail/{project_id}", name="获取项目详细")
async def select(project_id: Optional[int]):
    """
    - 获取指定项目ID详情接口\n
    - project_id: 项目ID
    """
    try:
        # 获取指定项目
        # 判断项目是否存在
        await models.Project.get(id=project_id)
        # 判断项目是否被删除
        is_deleted = await models.Project.filter(id=project_id, deleted=1)
        if is_deleted:
            return core.Fail(message="项目已被删除.")
        data = await models.Project_Pydantic.from_queryset_single(models.Project.get(id=project_id))
        return core.Success(data=data)
    except Exception as e:
        return core.Fail(message=f"项目不存在.")


@project_router.get("/project/getAllNoPage", name="获取所有项目不分页")
async def get_projects():
    """
    - 获取全部分页内容，不支持分页
    """
    # 按照不分页结构显示
    data = await models.Project_Pydantic.from_queryset(models.Project.filter(deleted=0).all())
    return core.Success(data={"total": len(data), "items": data})
