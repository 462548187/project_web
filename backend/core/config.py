"""
project: apiAutoTestWeb
file: config.py
author: zy7y
date: 2021/4/17
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

    # 启动端口配置
    PORT = 8999
    # 是否热加载
    RELOAD = True
    DEBUG = True

    # 接口文档设置
    TITLE: str = 'ProjectWeb'
    DESC: str = """
`接口自动化测试工具的可视化版本，将原本对用例的操作转移到Web页面之上`
- 前端：`Vue2`  `ElementUI`   `Vue element admin template`
- 后端: `Python` ` FastAPI ` `Tortoise ORM`  `MySQL`

**资料汇总**
- [x] [Gitee源码](https://gitee.com/zy7y/apiAutoTestWeb)

    """


setting = Settings()
