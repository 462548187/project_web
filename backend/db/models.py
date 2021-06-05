# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  model.py
@Description    :
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""
from typing import List
from enum import Enum

from tortoise import fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from .enum_filed import ContentType, Methods, Standard, StoryType


# 抽象模型类
class AbstractModel(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(255, description="名称")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractModel):
    username = fields.CharField(max_length=255, unique=True, description="用户名")
    password = fields.CharField(max_length=255, description="用户密码")
    nickname = fields.CharField(max_length=255, description="昵称")
    email = fields.CharField(max_length=255, description="邮箱", null=True)
    mobile = fields.CharField(max_length=255, description="手机", null=True)
    is_active = fields.BooleanField(max_length=255, description="是否激活", default=1)
    avatar = fields.CharField(max_length=255,
                              default="/static/default.jpg",
                              description="用户头像")


class Project(AbstractModel):
    name = fields.CharField(max_length=255, description="项目名称", unique=True)
    desc = fields.TextField(description="项目描述", null=True)
    front_serve = fields.TextField(description="前端服务", null=True)
    back_serve = fields.TextField(description="后端服务", null=True)

    # 查询集最大递归层级
    class PydanticMeta:
        max_recursion = 1


class Story(AbstractModel):
    name = fields.CharField(max_length=255, description="需求名称", unique=True)
    type = fields.CharEnumField(StoryType, default=StoryType.demand)
    project = fields.ForeignKeyField('models.Project', related_name='stories', description="所属业务")
    desc = fields.TextField(description="功能描述", null=True)
    dev_name = fields.CharField(max_length=255, description="开发人", null=True)
    test_name = fields.CharField(max_length=255, description="测试人", null=True)
    priority = fields.CharField(max_length=255, description="测试人", null=True)
    test_time = fields.DateField(auto_now_add=True, description="提测时间")
    online_time = fields.DateField(auto_now_add=True, description="上线时间")
    remark = fields.CharField(max_length=255, description="备注", null=True)

    class PydanticMeta:
        max_recursion = 2


class Push(AbstractModel):
    project = fields.ForeignKeyField('models.Project', related_name='pushes', description="所属业务")
    name = fields.CharField(max_length=255, description="事件名称", unique=True)
    receive = fields.CharField(max_length=255, description="接收方式", null=True)
    web_hook = fields.CharField(255, description="webhook", unique=True)
    template = fields.CharField(max_length=255, description="模板", null=True)
    is_active = fields.BooleanField(max_length=255, description="是否激活", default=1)

    class PydanticMeta:
        max_recursion = 2


# 解决pydantic_model_creator 生成的模型中 缺少外键关联字段
Tortoise.init_models(["db.models"], "models")

# 返回模型
User_Pydantic = pydantic_model_creator(User, name="User", exclude=["password"])

# 输入模型 exclude_readonly 只读字段 非必填
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude=["avatar"], exclude_readonly=True)

Project_Pydantic = pydantic_model_creator(Project, name="Project")
ProjectIn_Pydantic = pydantic_model_creator(
    Project, name="ProjectIn", exclude_readonly=True)

Story_Pydantic = pydantic_model_creator(Story, name="Story")
StoryIn_Pydantic = pydantic_model_creator(
    Story, name="StoryIn", exclude_readonly=True)

Push_Pydantic = pydantic_model_creator(Push, name="Push")
PushIn_Pydantic = pydantic_model_creator(
    Push, name="PushIn", exclude_readonly=True)
