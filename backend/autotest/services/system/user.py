"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:20
"""
import uuid
from datetime import datetime
from loguru import logger

from autotest.models.system_models import User
from autotest.schemas.system.user import UserLogin, UserTokenIn
from autotest.utils.decrypt import decrypt_rsa_password
from autotest.utils.response_code import CodeEnum
from autotest.utils.serialize import default_serialize


class UserService:
    """
    用户服务类
    """

    @staticmethod
    async def login(params: UserLogin) -> UserTokenIn:
        """
        登录
        :param params:
        :return:
        """
        username = params.username
        password = params.password
        if not username or not password:
            raise ValueError(CodeEnum.PARTNER_CODE_PARAMS_FAIL.msg)
        user_info = await User.get_user_by_name(username)
        if not user_info:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = decrypt_rsa_password(user_info['password'])
        if u_password != password:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)

        logger.info('用户 [{}] 登录了系统'.format(user_info["username"]))

