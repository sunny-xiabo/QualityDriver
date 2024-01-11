"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: roles.py
# @Date: 2024/1/2 19:50
"""
import typing

from pydantic import BaseModel, Field, root_validator

from autotest.schemas.base import BaseSchema


class RoleInfo(BaseModel):
    id: int = Field(None, description="角色id")
    name: str = Field(..., description="角色名称")
    role_type: int = Field(default=10, description="角色类型")
    menus:str = Field(..., description="菜单")
    description: str = Field(None, description="角色描述")
    status: int = Field(default=0, description="角色状态 0-正常 1-禁用")

    @root_validator(pre=True)
    def root_validator(cls, data: typing.Dict[typing.Text, typing.Any]):
        """
        校验
        :param data:
        :return:
        """
        menus = data.get("menus",[])
        if menus:
            data["menus"] = ','.join(list(map(str,menus)))
        return data

class RoleQuery(BaseSchema):
    id: int = Field(None, description="角色id")
    name: str = Field(None, description="角色名称")
    role_type: int = Field(10, description="角色类型")

class RoleDel(BaseModel):
    id: int = Field(..., description="角色id")
