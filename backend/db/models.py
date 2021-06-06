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
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from .enum_filed import StoryType


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
    avatar = fields.CharField(max_length=255, default="/static/default.jpg", description="用户头像")


class Project(AbstractModel):
    name = fields.CharField(max_length=255, description="项目名称", unique=True)
    desc = fields.TextField(description="项目描述", null=True)
    front_serve = fields.TextField(description="前端服务", null=True)
    back_serve = fields.TextField(description="后端服务", null=True)

    # 查询集最大递归层级
    class PydanticMeta:
        max_recursion = 1


class Story(AbstractModel):
    project = fields.ForeignKeyField('models.Project', related_name='story_router', description="项目ID")
    name = fields.CharField(max_length=255, description="需求名称", unique=True)
    type = fields.CharEnumField(StoryType, default=StoryType.demand, description="需求类型")
    desc = fields.TextField(description="需求描述", null=True)
    stroy_path = fields.CharField(max_length=255, description="需求链接", null=True, default="")
    stroy_name = fields.CharField(max_length=255, description="需求人", null=True)
    dev_name = fields.CharField(max_length=255, description="开发人", null=True)
    test_name = fields.CharField(max_length=255, description="测试人", null=True)
    stroy_priority = fields.CharField(max_length=255, description="需求优先级", null=True)
    review_time = fields.DateField(description="评审时间", null=True)
    confirm_time = fields.DateField(description="交底时间", null=True)
    status = fields.IntField(max_length=1, description="需求状态", default='0')
    remark = fields.TextField(description="备注", null=True)

    class PydanticMeta:
        max_recursion = 2


class Task(AbstractModel):
    stroy_id = fields.ForeignKeyField('models.Story', related_name='task_router', description="需求ID")
    task_priority = fields.CharField(max_length=255, description="任务优先级", null=True)
    test_time = fields.DateField(description="提测时间", null=True)
    online_time = fields.DateField(description="上线时间", null=True)
    server = fields.CharField(max_length=255, description="发布服务", null=True)
    status = fields.IntField(max_length=1, description="任务状态", default='0')
    remark = fields.TextField(description="备注", null=True)

    class PydanticMeta:
        max_recursion = 2


class Push(AbstractModel):
    project = fields.ForeignKeyField('models.Project', related_name='push_router', description="所属业务")
    name = fields.CharField(max_length=255, description="事件名称", unique=True)
    receive = fields.CharField(max_length=255, description="接收方式", null=True)
    web_hook = fields.CharField(255, description="webhook", unique=True)
    template = fields.CharField(max_length=255, description="模板", null=True)
    is_active = fields.BooleanField(max_length=255, description="是否激活", default=1)

    class PydanticMeta:
        max_recursion = 2


# 解决pydantic_model_creator 生成的模型中 缺少外键关联字段
# Tortoise.init_models(["db.models"], "models")

# 返回模型
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))

# 输入模型 exclude_readonly 只读字段 非必填
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude=("avatar",), exclude_readonly=True)

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
