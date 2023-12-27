"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: cors.py
# @Date: 2023/12/27 13:01
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import config


def init_cors(app: FastAPI):
    """
    初始化跨域
    :param app:
    :return:
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins = [str(origin) for origin in config.CORS_ORIGINS],
        allow_credentials = True,       # 允许发送 cookies
        allow_methods = ["*"],          # 允许请求方法
        allow_headers = ["*"],          # 允许请求头
    )