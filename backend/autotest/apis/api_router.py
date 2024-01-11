"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: api_router.py
# @Date: 2023/12/16 21:29
"""

from fastapi import APIRouter

from autotest.apis.system import user, role

app_router = APIRouter()



# system
app_router.include_router(user.router, prefix="/user", tags=['user'])
app_router.include_router(role.router, prefix="/roles", tags=['roles'])

#dd