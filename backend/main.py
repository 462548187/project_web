# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  main.py
@Description    :  主入口
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""

from api import create_app
from core.config import settings
import uvicorn

# uvicorn main:app --reload 启动
app = create_app()

if __name__ == '__main__':
    # uvicorn.run("main:app", host="0.0.0.0", reload=True)
    uvicorn.run(app="main:app", host="127.0.0.1", port=settings.PORT, reload=settings.RELOAD, debug=settings.DEBUG)
