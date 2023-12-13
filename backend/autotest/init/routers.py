"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: routers.py
# @Date: 2023/12/11 18:18
"""

from fastapi import FastAPI
from config import config
from autotest.apis import app_router


def init_router(app: FastAPI):
    """
    初始化路由
    :param app:
    :return:
    """

    app.include_router(app_router, prefix=config.API_PREFIX)
