# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  main.py
@Description    :
@CreateTime     :  2021/5/29, 11:44
------------------------------------
@ModifyTime     :
"""

from api import create_app

# uvicorn main:app --reload 启动
app = create_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
