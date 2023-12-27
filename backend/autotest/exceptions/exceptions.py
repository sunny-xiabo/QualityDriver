"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: exceptions.py
# @Date: 2023/12/12 16:25
"""

import typing

from autotest.utils.response_code import CodeEnum


class MyBaseException(Exception):
    """
    自定义异常
    """

    def __init__(self, error_or_code: typing.Union[CodeEnum, str]):
        if isinstance(error_or_code, CodeEnum):
            code = error_or_code.code
            msg = error_or_code.msg
        else:
            code = CodeEnum.PARTNER_CODE_FAIL.code
            msg = error_or_code
        self.code = code
        self.msg = msg


class AccessTokenFail(MyBaseException):
    """
    访问令牌失败
    """

    def __init__(self, code: str = CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.code,
                 msg: str = CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg):
        super(AccessTokenFail, self).__init__(code)
        self.msg = msg

class SetRedis(MyBaseException):
    """
    设置redis失败
    """
    def __init__(self):
        super(SetRedis, self).__init__("Redis存储失败")

class UserNotExist(MyBaseException):
    """
    用户不存在
    """
    def __init__(self):
        super(UserNotExist, self).__init__("用户不存在")

class ErrorUser(MyBaseException):
    """
    错误的用户或密码
    """
    def __init__(self):
        super(ErrorUser, self).__init__("错误的用户名或密码")

class PermissionNotEnough(MyBaseException):
    """
    权限不足
    """
    def __init__(self):
        super(PermissionNotEnough, self).__init__("权限不足,拒绝访问")

class ParameterError(MyBaseException):
    """
    参数错误
    """
    def __init__(self, err_code: typing.Union[CodeEnum, str]):
        super(ParameterError, self).__init__(err_code)

class EnvConfigInitError(MyBaseException):
    """
    环境配置初始化错误
    """
    def __init__(self, err_code: typing.Union[CodeEnum, str]):
        super(EnvConfigInitError, self).__init__(err_code)