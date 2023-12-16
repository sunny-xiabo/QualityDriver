"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:01
"""
from fastapi import APIRouter

from autotest.schemas.system.user import UserLogin
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