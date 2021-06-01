"""
project: apiAutoTestWeb
file: main.py
author: zy7y
date: 2021/4/17
"""

from api import create_app
from core.config import setting
import uvicorn

# uvicorn main:app --reload 启动
app = create_app()

if __name__ == '__main__':
    # uvicorn.run("main:app", host="0.0.0.0", reload=True)
    uvicorn.run(app="main:app", host='0.0.0.0', port=setting.PORT, reload=setting.RELOAD)
