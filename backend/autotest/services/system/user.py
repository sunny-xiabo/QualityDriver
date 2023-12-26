"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: user.py
# @Date: 2023/12/12 11:20
"""
import traceback
import typing
import uuid
from datetime import datetime
from loguru import logger

from autotest.models.system_models import User
from autotest.schemas.system.user import UserLogin, UserTokenIn, UserInfo, UserResetPwd, UserDel
from autotest.utils.consts import CACHE_DAY, TEST_USER_INFO
from autotest.utils.decrypt import decrypt_rsa_password, encrypt_rsa_password
from autotest.utils.local import g
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
            raise ValueError(CodeEnum.PARTNER_CODE_PARAMS_FAIL.code,
                             CodeEnum.PARTNER_CODE_PARAMS_FAIL.msg)
        user_info = await User.get_user_by_name(username)
        if not user_info:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.code,
                             CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = decrypt_rsa_password(user_info['password'])
        if u_password != password:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.code,
                             CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        token = str(uuid.uuid4())
        login_time = default_serialize(datetime.now())
        token_user_info = UserTokenIn(
            id=user_info["id"],
            token=token,
            avatar=user_info["avatar"],
            username=user_info["username"],
            nickname=user_info["nickname"],
            roles=user_info.get("roles", []),
            tags=user_info.get("tags", []),
            login_time=login_time,
            remarks=user_info["remarks"]
        )
        await g.redis.set(TEST_USER_INFO.format(token), token_user_info.dict(), CACHE_DAY)
        logger.info('用户 [{}] 登录了系统'.format(user_info["username"]))

    @staticmethod
    async def logout():
        """
        退出
        :return:
        """
        token = g.request.headers.get("token")
        try:
            # 从Redis中删除与该token关联的用户信息
            await g.redis.delete(TEST_USER_INFO.format(token))
            return "退出成功"
        except Exception as e:
            # 记录错误信息并返回错误原因
            error_message = traceback.format_exc()
            logger.error(error_message)
            return "退出失败: {}".format(error_message)

    @staticmethod
    async def user_register(user_params: UserInfo) -> "User":
        """
        用户注册
        :param user_params:
        :return:
        """
        user_info = await User.get_user_by_name(user_params.username)
        if user_info:
            raise ValueError(CodeEnum.USERNAME_OR_EMAIL_IS_REGISTERED.code,
                             CodeEnum.USERNAME_OR_EMAIL_IS_REGISTERED.msg)
        user = await User.create(user_params.dict())
        return user

    @staticmethod
    async def check_token(token: str) -> typing.Dict[str, typing.Any]:
        """
        校验token
        :param token: 用户的token，应该是一个字符串
        :return: 一个字典，包含用户的 ID 和用户名。如果 token 无效或 None，将引发一个异常
        """
        if token is None:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_IS_NONE.code, CodeEnum.PARTNER_CODE_TOKEN_IS_NONE.msg)

        user_info = await g.redis.get(TEST_USER_INFO.format(token))
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.code,
                             CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)

        if not isinstance(user_info, dict):
            raise TypeError(f"Unexpected type for user_info: {type(user_info).__name__}")

        user_info = {
            "id": user_info.get("id", None),
            "username": user_info.get("username", None),
        }
        return user_info

    @staticmethod
    async def reset_password(params: UserResetPwd):
        """
        重置密码
        :param params:
        :return:
        """
        if params.new_pwd != params.re_new_pwd:
            raise ValueError(CodeEnum.PASSWORD_TWICE_IS_NOT_AGREEMENT.code,
                             CodeEnum.PASSWORD_TWICE_IS_NOT_AGREEMENT.msg)
        user_info = await User.get(params.id)
        pwd = decrypt_rsa_password(user_info.password)
        if params.old_pwd != pwd:
            raise ValueError(CodeEnum.OLD_PASSWORD_ERROR.code,
                             CodeEnum.OLD_PASSWORD_ERROR.msg)
        if params.new_pwd == pwd:
            raise ValueError(CodeEnum.NEW_PWD_NO_OLD_PWD_EQUAL.code,
                             CodeEnum.NEW_PWD_NO_OLD_PWD_EQUAL.msg)
        new_pwd = encrypt_rsa_password(params.new_pwd)
        await User.create_or_update({"id": params.id, "password": new_pwd})

    @staticmethod
    async def deleted_user(params: UserDel):
        """
        删除用户
        :param params: ID
        :return:
        """
        try:
            return await User.delete(params.id)
        except Exception as e:
            logger.error(traceback.format_exc())

