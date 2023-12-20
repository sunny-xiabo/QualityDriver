"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: current_user.py
# @Date: 2023/12/20 15:47
"""
import typing

from autotest.exceptions.exceptions import AccessTokenFail
from autotest.init.redis_init import init_async_redis_pool
from autotest.utils.consts import TEST_USER_INFO
from autotest.utils.local import g


async def current_user(token: str = None) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
    """
    根据token获取当前用户信息
    :param token:
    :return:
    """
    if not g.redis:
        g.redis = await init_async_redis_pool()
    user_info = await g.redis.get(TEST_USER_INFO.format(g.token if not token else token))
    if not user_info:
        raise AccessTokenFail()
    return user_info
