"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: api_router.py
# @Date: 2023/12/16 21:29
"""

from fastapi import APIRouter

from autotest.apis.system import user

app_router = APIRouter()



# system
app_router.include_router(user.router, prefix="/user", tags=['user'])