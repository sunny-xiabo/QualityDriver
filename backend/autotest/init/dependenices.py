"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: dependencies.py
# @Date: 2023/12/19 19:50
"""
from fastapi.security import APIKeyHeader
from fastapi import Request, Security


from autotest.exceptions.exceptions import AccessTokenFail
from autotest.utils.consts import TEST_USER_INFO, CACHE_DAY
from autotest.utils.local import g
from config import config


class MyAPIKeyHeader(APIKeyHeader):
    """
    自定义APIKeyHeader
    """

    def __init__(self):
        super().__init__(name="token", auto_error=False)

    async def __call__(self, request: Request):
        g.request = request
        path: str = request.get('path')
        if path in config.WHITE_ROUTER:
            return
        token: str = request.headers.get("token")
        if not token:
            raise AccessTokenFail()
        user_info_key= TEST_USER_INFO.format(token)
        user_info = await g.redis.get(user_info_key)
        if not user_info:
            raise AccessTokenFail()
        # 重置token时间
        await g.redis.set(user_info_key, user_info, CACHE_DAY)
        return


async def login_verification(token: Security = Security(MyAPIKeyHeader())):
    """
    登录校验
    :param token: token
    :return:
    """
    pass
