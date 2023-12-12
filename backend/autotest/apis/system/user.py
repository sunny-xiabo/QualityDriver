"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:01
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/login", description="登录")
async def login():
    """
    登录
    :return:
    """
    pass
