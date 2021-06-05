#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@Project: apiAutoTestFastApi
@File  :util.py
@Author:liuyue
@Date  :2021/4/28 10:54
@Desc  : 其他工具路由
"""
from tortoise.transactions import in_transaction

import core
from core import MysqlSettings
from db import models
from util import read_file

from fastapi import APIRouter

from util.wr_file import write_file

util_router = APIRouter(tags=["其他"])


@util_router.get("/help", name="获取说明文档")
async def help_doc():
    return core.Success(data=await read_file('apiAutoTestWeb使用说明.md'))


@util_router.get("/code", name="获取扩展脚本")
async def get_code():
    return core.Success(data=await read_file('util/extend.py'))


@util_router.put("/code", name="修改扩展脚本")
async def update_code(script: core.Code):
    # 验证是否可以被执行
    try:
        exec(script.code)
        await write_file('util/extend.py', script.code)
        return core.Success()
    except Exception as e:
        return core.Fail(message=f"更新失败.{e}")


@util_router.get("/list", name="平台数据获取")
async def get_plant():
    # 获取当天数据 总数 SELECT count(*) FROM project WHERE  strftime('%Y-%m-%d',
    # created_at) = date('now')
    tables = ['project']
    today = []
    async with in_transaction("default") as conn:
        for table in tables:
            data = await conn.execute_query_dict(f"SELECT count(*) as total FROM {table} WHERE  strftime('%Y-%m-%d', created_at) = date('now')")
            today.append(data[0]["total"])
    return core.Success(data={
        "project": len(await models.Project.all()),
        "today": today
    })
