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
    def __init__(self):
        super(AccessTokenFail, self).__init__(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL)
