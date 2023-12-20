"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: redis_init.py
# @Date: 2023/12/16 20:17
"""
import typing

from fastapi import FastAPI

from config import config
from autotest.db.db_redis import MyAsyncRedis

Qredis = None


async def init_async_redis_pool(app: typing.Optional[FastAPI] = None) -> MyAsyncRedis:
    """连接redis"""
    global Qredis
    redis = await MyAsyncRedis.from_url(url=config.REDIS_URI)
    Qredis = redis
    if app is not None:
        app.state.redis = redis
    return redis
