"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:01
"""
from fastapi import APIRouter, Request

from autotest.schemas.system.user import UserLogin, UserInfo, UserResetPwd, UserDel
from autotest.services.system.user import UserService
from autotest.utils.response_http_response import partner_success

router = APIRouter()


@router.post("/login", description="登录")
async def login(params: UserLogin):
    """
    登录
    :return:
    """
    try:
        data = await UserService.login(params)
        return partner_success(data, msg="登录成功")
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)


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
    try:
        data = await UserService.user_register(user_info)
        return partner_success(data, msg="注册成功")
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)


@router.post("/authorizeToken", description="校验token")
async def authorize_token(request: Request):
    """
    校验token
    :param request:
    :return:
    """
    try:
        token = request.headers.get("token", None)
        user_info = await UserService.check_token(token)
        return partner_success(user_info, msg="校验成功")
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)


@router.post("/resetPassword", description="重置密码")
async def reset_password(params: UserResetPwd):
    """
    重置密码
    :param params:
    :return:
    """
    try:
        await UserService.reset_password(params)
        return partner_success()
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)


@router.post("/deletedUser", description="删除用户")
async def deleted_user(params: UserDel):
    """
    删除用户
    :param params:
    :return:
    """
    try:
        data = await UserService.deleted_user(params)
        return partner_success(data, msg="删除成功")
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)


@router.post("/getUserInfoByToken", description="通过token获取用户信息")
async def get_user_info_by_token(request: Request):
    """
    通过token获取用户信息
    :param request:
    :return:
    """
    try:
        token = request.headers.get("token", None)
        user_info = await UserService.get_user_info_by_token(token)
        return partner_success(user_info)
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)
