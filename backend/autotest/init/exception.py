"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: exception.py
# @Date: 2023/12/27 13:13
"""
import traceback

from fastapi import FastAPI
from loguru import logger
from starlette.requests import Request

from autotest.utils.response_code import CodeEnum
from autotest.utils.response_http_response import partner_success


def init_exception(app: FastAPI):
    """
    全局异常捕获
    :param app:
    :return:
    """

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """ 捕获全局异常 """
        # 详细的日志记录
        logger.error(
            f"全局异常\n"
            f"{request.method} "
            f"URL:{request.url}\n"
            f"Headers:{request.headers}\n"
            f"{traceback.format_exc()}")

        # 具体的错误消息
        msg = str(exc)

        return partner_success(code=CodeEnum.PARTNER_CODE_FAIL.code, msg=msg,
                               headers={'Access-Control-Allow-Origin': '*'})
