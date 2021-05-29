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
import secrets
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """配置类"""

    # token相关
    ALGORITHM: str = "HS256"  # 加密算法
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 随机生成的base64位字符串
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # token的时效 3 天 = 60 * 24 * 3

    # 跨域设置
    ORIGINS: List[str] = ["*"]

    # 接口文档设置
    DESC: str = """
    `apiAutoTest接口自动化测试工具的可视化版本，将原本对用例的操作转移到Web页面之上`
    - 前端：`Vue2`  `ElementUI`   `Vue element admin template`
    - 后端: `Python` ` FastAPI ` `Tortoise ORM`  `Sqlite3`
    
    **资料汇总**
    - [x] [Github源码](https://github.com/462548187/project_web)
    """


setting = Settings()
