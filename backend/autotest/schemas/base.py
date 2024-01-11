"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: base.py
# @Date: 2024/1/2 19:59
"""
from pydantic import BaseModel, validator


class BaseSchema(BaseModel):
    """
    基础查询参数
    """
    def dict(self, *args, **kwargs):
        """
        转换为字典
        :param args:
        :param kwargs:
        :return:
        """
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        return super(BaseSchema, self).dict(*args, **kwargs)


    @validator('*', pre=True)
    def blank_string(cls, v):
        if v == '':
            return None
        return v
