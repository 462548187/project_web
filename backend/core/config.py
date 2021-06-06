# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  config.py
@Description    :
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""
import os
import secrets
import time
from loguru import logger
from pydantic import AnyHttpUrl
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """配置类"""
    ENV = os.environ.get("fast_env", "DEV")  # 本次启动环境
    APP_NAME = "fastapi-vue-admin"
    # api前缀
    API_PREFIX = "/v1"
    # token相关
    ALGORITHM: str = "HS256"  # 加密算法
    # jwt密钥,建议随机生成一个
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 随机生成的base64位字符串
    # token过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # token的时效 3 天 = 60 * 24 * 3

    # 跨域设置
    ORIGINS: List[str] = ["*"]

    # 跨域白名单
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000"]

    # db配置
    DB_URL = "mysql://root:123456@127.0.0.1:3306/project_web"

    # 启动端口配置
    PORT = 8999
    # 是否热加载
    RELOAD = True
    DEBUG = False

    # 接口文档设置
    TITLE: str = 'ProjectWeb'
    DESC: str = """
    `测试部门日常项目信息同步工具`
    - 前端：`Vue2`  `ElementUI`   `Vue element admin template`
    - 后端: `Python` ` FastAPI ` `Tortoise ORM`  `MySQL`
    
    **资料汇总**
    - [x] [Github源码](https://github.com/462548187/project_web)

    """

    # 日志收集器
    # LOG_FOLDER = "D:\\code\\fastapi-logs"
    LOG_FOLDER = "./fastapi-logs"
    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)
    t = time.strftime("%Y_%m_%d")
    # logger = logger
    logger.add(f"{LOG_FOLDER}/fastapi_log_{t}.log", rotation="00:00", encoding="utf-8", retention="30 days")

    DINGDING_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=26c3772451872f111251362e908a7cae0ff49814d54f861d54d0ed2c8eb18e44'
    DINGDING_SECRET = 'SEC43f155e2fbeab82d83ea48ada18218dcfd4cb73d09de1ecb491d167890e7e451'
    USER_CREATE_MSG = '测试中台系统推送:账号:{},密码：{}'


settings = Settings()
