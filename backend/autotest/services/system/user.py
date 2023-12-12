"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:20
"""
from autotest.models.system_models import User
from autotest.schemas.system.user import UserLogin, UserTokenIn


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
            raise ValueError("用户名或密码不能为空")
        user_info = await User.get_by_username(username)