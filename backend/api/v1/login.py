"""
project: apiAutoTestWeb
file: login.py
author: liuyue
date: 2021/4/17
desc: 鉴权处理
"""
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
import core
from db import models

login_router = APIRouter(tags=["登录相关"])


@login_router.post("/login", name="登录")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    """
    获取token
    """
    user_obj = await models.User.get(username=user.username)

    if not core.verify_password(user.password, user_obj.password):
        logger.error("账号密码错误!!!")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="帐号或密码错误",
            headers={"WWW-Authenticate": "Bearer"}, )

    if not user_obj.is_active:
        logger.error(f"{user.username}未激活")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="用户未激活!!!",
            headers={"WWW-Authenticate": "Bearer"}, )

    if user_obj and core.verify_password(user.password, user_obj.password):
        access_token = core.create_access_token({"sub": user_obj.username})

        return JSONResponse({"access_token": access_token, "token_type": "bearer"})


@login_router.post("/logout", name="退出")
async def logout(token: str = Depends(core.get_current_user)):
    return core.Success(data=token)
