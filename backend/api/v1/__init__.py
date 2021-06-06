# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  __init__.py
@Description    :
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""
import core
from .user import user_router
from .staff import staff_router
from .project import project_router
from .story import story_router
from .push import push_router
from .task import task_router
from fastapi import APIRouter, Depends

# v1 = APIRouter(prefix="/v1", dependencies=[Depends(core.get_current_user)])
v1 = APIRouter(prefix="/v1")

v1.include_router(user_router)
v1.include_router(staff_router)
v1.include_router(project_router)
v1.include_router(story_router)
v1.include_router(task_router)
v1.include_router(push_router)
