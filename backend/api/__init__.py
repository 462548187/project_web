"""
project: apiAutoTestWeb
file: __init__.py
author: liuyue
date: 2021/4/17
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from core import settings
from api.v1.login import login_router

# from db import log


# 导入子路由
from .v1 import v1


def create_app():
    # 初始化app实例
    if settings.ENV == "PROD":
        # 生产关闭swagger
        app = FastAPI(title=settings.APP_NAME, docs_url=None, redoc_url=None)
    else:
        app = FastAPI(title=settings.TITLE, description=settings.DESC)

    # 挂载静态文件
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # 挂载 数据库
    register_tortoise(
        app,
        db_url=settings.DB_URL,
        modules={"models": ["db.models"]},
        # 生成表
        generate_schemas=True,
        # 使用异常，当无数据是自动返回
        add_exception_handlers=True,
    )

    # 设置CORS站点
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(CORSMiddleware,
                           allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
                           # allow_origins=settings.ORIGINS,
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"],
                           expose_headers=["Content-Disposition"]
                           )

    # 挂载子路由
    app.include_router(prefix="/v1", router=login_router)
    app.include_router(router=v1)

    return app
