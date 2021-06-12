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
from fastapi import APIRouter

project_router = APIRouter(tags=['项目相关'])


@project_router.post("/project/add", name="项目新增编辑")
async def update(project: models.ProjectInBase):
    """
    - 新增和编辑项目的接口，项目名称name为必须传参数\n
    - name: 项目名称
    - 没有项目名称会新增项目信息，如果有项目名称会编辑项目信息
    """
    try:
        # 判断项目是否被删除
        is_deleted = await models.Project.filter(name=project.name, deleted=1)
        # 判断项目是否被激活
        is_status = await models.Project.filter(name=project.name, status=0)
        if is_deleted:
            return core.Fail(message="项目已被删除.")
        elif is_status:
            return core.Fail(message="项目未被激活.")
        # 创建或更新项目
        else:
            # 判断项目是否存在，存在就编辑，不存在就新增
            if await models.Project.filter(name=project.name):
                await models.Project.filter(name=project.name).update(**project.dict(exclude_unset=True))
                return core.Success(data=await models.Project_Pydantic.from_queryset_single(models.Project.get(name=project.name)))
            else:
                try:
                    project_obj = await models.Project.create(**project.dict(exclude_unset=True))
                    return core.Success(data=await models.Project_Pydantic.from_tortoise_orm(project_obj))
                except Exception as e:
                    return core.Fail(message=f"创建失败.{e}")

    except Exception as e:
        return core.Fail(message="项目已存在.")


@project_router.delete("/project/del", name="删除项目")
async def delete(project: models.ProjectInBase):
    """
    - 删除项目的接口\n
    - name: 项目名称【必填】
    - 只需要传递需要删除的项目名称 name 字段
    """
    try:
        # 判断项目是否存在
        await models.Project.get(name=project.name)
        # 判断项目是否被删除
        is_deleted = await models.Project.filter(name=project.name, deleted=1)
        if is_deleted:
            return core.Fail(message="项目已被删除.")
        # 更新项目是否删除为1
        await models.Project.filter(name=project.name).update(deleted=1)
        return core.Success()
    except Exception as e:
        return core.Fail(message="项目不存在.")


@project_router.post("/project/res", name="恢复项目")
async def restore(project: models.ProjectInBase):
    """
    - 恢复项目的接口\n
    - name: 项目名称【必填】
    - 只需要传递需要恢复的项目名称 name字段
    """
    try:
        # 判断项目是否存在
        await models.Project.get(name=project.name)
        # 判断项目是否被删除
        is_deleted = await models.Project.filter(name=project.name, deleted=0)
        if is_deleted:
            return core.Fail(message="项目未被删除.")
        # 更新项目是否删除为1
        await models.Project.filter(name=project.name).update(deleted=0)
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


@project_router.post("/project/detail", name="获取项目详细")
async def select(project: models.ProjectInBase):
    """
    - 获取指定项目名称详情接口\n
    - name: 项目名称【必填】
    """
    try:
        # 获取指定项目
        # 判断项目是否存在
        await models.Project.get(name=project.name)
        # 判断项目是否被删除
        is_deleted = await models.Project.filter(name=project.name, deleted=1)
        # 判断项目是否被激活
        is_status = await models.Project.filter(name=project.name, status=0)
        if is_deleted:
            return core.Fail(message="项目已被删除.")
        elif is_status:
            return core.Fail(message="项目未被激活.")
        else:
            try:
                data = await models.Project_Pydantic.from_queryset_single(models.Project.get(name=project.name))
                return core.Success(data=data)
            except Exception as e:
                return core.Fail(message=f"打开项目详情失败.{e}")
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
