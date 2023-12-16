"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: middleware.py
# @Date: 2023/12/16 20:13
"""
import time

from fastapi import FastAPI, Request
from loguru import logger

from autotest.utils.common import get_str_uuid
from autotest.utils.local import g


def init_middleware(app: FastAPI):
    """
    中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def intercept(request: Request, call_next):
        g.trace_id = get_str_uuid()
        start_time = time.time()
        token = request.headers.get("token", None)
        g.redis = app.state.redis
        g.token = token
        remote_addr = request.headers.get("X-Real-IP", request.client.host)
        logger.info(f"访问记录:IP:{remote_addr}-method:{request.method}-url:{request.url}")
        response = await call_next(request)
        response.headers["X-request-id"] = g.trace_id
        return response