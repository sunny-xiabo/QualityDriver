"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: main.py
# @Date: 2023/12/11 16:47
"""
import click
import uvicorn
from fastapi import FastAPI, Depends
from loguru import logger

from autotest.init.cors import init_cors
from autotest.init.exception import init_exception
from autotest.init.logger_init import init_logger
from config import config
from autotest.init.routers import init_router
from autotest.init.redis_init import init_async_redis_pool
from autotest.init.middleware import init_middleware
from autotest.init.dependenices import login_verification

# 创建FastAPI应用
app = FastAPI(title="Quality Driver", version=config.PROJECT_VERSION, dependencies=[Depends(login_verification)])


async def init_app():
    """
    注册中心
    :return:
    """
    init_exception(app)  # 注册全局异常

    init_router(app)  # 注册路由

    init_middleware(app)  # 注册中间件

    init_cors(app)  # 注册初始化跨域

    await init_async_redis_pool(app)  # 连接redis

    init_logger()  # 初始化日志

    logger.info("日志启动成功")


@app.on_event("startup")
async def startup():
    click.echo(config.PROJECT_LOGO)
    await init_app()
    # from autotest.models import init_db
    # await init_db()


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=8101, reload=True)
