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
from .enum_filed import PriorityType, ReceiveType, StoryType


# 抽象模型类
class AbstractModel(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(255, description="名称")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractModel):
    username = fields.CharField(max_length=20, unique=True, description="用户名")
    password = fields.CharField(max_length=255, description="用户密码")
    is_active = fields.BooleanField(description="是否激活", default='1')
    avatar = fields.CharField(max_length=255, default="/static/default.jpg", description="用户头像")


class Staff(AbstractModel):
    name = fields.CharField(max_length=25, unique=True, description="员工姓名")
    email = fields.CharField(max_length=50, description="邮箱", null=True)
    mobile = fields.CharField(max_length=11, description="手机", null=True)
    department = fields.CharField(max_length=20, description="部门", null=True)
    status = fields.BooleanField(description="是否在职", default='1')


class Project(AbstractModel):
    name = fields.CharField(max_length=20, description="项目名称", unique=True)
    desc = fields.TextField(description="项目描述", null=True)
    front_serve = fields.TextField(description="前端服务", null=True)
    back_serve = fields.TextField(description="后端服务", null=True)
    status = fields.IntField(max_length=1, description="需求状态", default='1')

    # 查询集最大递归层级
    class PydanticMeta:
        max_recursion = 1


class Story(AbstractModel):
    name = fields.CharField(max_length=20, description="需求名称", unique=True)
    project = fields.ForeignKeyField('models.Project', related_name='story_router', description="项目ID")
    type = fields.CharEnumField(StoryType, default=StoryType.Demand, description="需求类型")
    desc = fields.TextField(description="需求描述", null=True)
    stroy_path = fields.CharField(max_length=255, description="需求链接", null=True, default="")
    stroy_priority = fields.CharEnumField(PriorityType, default=PriorityType.Default, description="优先级")
    status = fields.IntField(max_length=1, description="需求状态", default='1')
    remark = fields.TextField(description="备注", null=True)

    class PydanticMeta:
        max_recursion = 2


class Task(AbstractModel):
    name = fields.CharField(max_length=20, description="任务名称", unique=True)
    stroy = fields.ForeignKeyField('models.Story', related_name='task', description="需求ID")
    task_priority = fields.CharEnumField(PriorityType, default=PriorityType.Default, description="优先级")
    stroy_name = fields.ManyToManyField('models.Staff', related_name='task', through='task_story', description="产品员工ID")
    dev_name = fields.ManyToManyField('models.Staff', related_name='task1', through='task_dev', description="开发员工ID")
    tester_name = fields.ManyToManyField('models.Staff', related_name='task2', through='task_tester', description="测试员工ID")
    review_time = fields.DateField(description="评审时间", null=True)
    confirm_time = fields.DateField(description="交底时间", null=True)
    test_time = fields.DateField(description="提测时间", null=True)
    online_time = fields.DateField(description="上线时间", null=True)
    server = fields.CharField(max_length=255, description="发布服务", null=True)
    status = fields.IntField(max_length=1, description="任务状态", default='1')
    remark = fields.TextField(description="备注", null=True)

    class PydanticMeta:
        max_recursion = 2


class Push(AbstractModel):
    name = fields.CharField(max_length=20, description="推送名称", unique=True)
    project = fields.ForeignKeyField('models.Project', related_name='push', description="项目ID")
    receive = fields.CharEnumField(ReceiveType, default=ReceiveType.Dingding, description="接收方式")
    web_hook = fields.CharField(max_length=255, description="webhook", null=True)
    secret = fields.CharField(max_length=255, description="secret", null=True)
    template = fields.CharField(max_length=255, description="模板", null=True)
    at_name = fields.ManyToManyField('models.Staff', related_name='push1', through='push_staff', description="通知自定义人")
    at_all = fields.BooleanField(description="通知所有人", default='0')
    is_active = fields.BooleanField(description="是否激活", default='1')

    class PydanticMeta:
        max_recursion = 2


# 解决pydantic_model_creator 生成的模型中 缺少外键关联字段
Tortoise.init_models(["db.models"], "models")

# 返回模型
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))

# 输入模型 exclude_readonly 只读字段 非必填
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude=("avatar",), exclude_readonly=True)

# 项目相关
Staff_Pydantic = pydantic_model_creator(Staff, name="Staff")
StaffIn_Pydantic = pydantic_model_creator(Staff, name="StaffIn", exclude_readonly=True)

# 项目相关
Project_Pydantic = pydantic_model_creator(Project, name="Project")
ProjectIn_Pydantic = pydantic_model_creator(Project, name="ProjectIn", exclude_readonly=True)

# 需求相关
Story_Pydantic = pydantic_model_creator(Story, name="Story")
StoryIn_Pydantic = pydantic_model_creator(Story, name="StoryIn", exclude_readonly=True)

# 任务相关
Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)

# 推送相关
Push_Pydantic = pydantic_model_creator(Push, name="Push")
PushIn_Pydantic = pydantic_model_creator(Push, name="PushIn", exclude_readonly=True)


class TaskInStroyName(TaskIn_Pydantic):
    stroy_name_list: List[int]
    stroy_dev_list: List[int]
    stroy_tester_list: List[int]


class PushInName(PushIn_Pydantic):
    push_name_list: List[int]
