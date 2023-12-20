"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:01
"""
from fastapi import APIRouter

from autotest.schemas.system.user import UserLogin, UserInfo
from autotest.services.system.user import UserService
from autotest.utils.response_http_response import partner_success

router = APIRouter()


@router.post("/login", description="登录")
async def login(params: UserLogin):
    """
    登录
    :return:
    """
    data = await UserService.login(params)
    return partner_success(data, msg="登录成功")

@router.post("/logout", description="退出")
async def logout():
    """
    退出
    :return:
    """
    await UserService.logout()
    return partner_success()

@router.post("/userRegister", description="用户注册")
async def user_register(user_info: UserInfo):
    """
    用户注册
    :return:
    """
    data = await UserService.user_register(user_info)
    return partner_success(data, msg="注册成功")