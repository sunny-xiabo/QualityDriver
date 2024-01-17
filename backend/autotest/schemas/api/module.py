"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: module.py
# @Date: 2024/1/17 19:55
"""

import typing

from pydantic import Field, BaseModel
from autotest.schemas.base import BaseSchema


class ModuleInfo(BaseSchema):
    """
    模块信息序列化
    """
    id: int = Field(None, description="模块id")
    name: str = Field(..., description="模块名称")
    project_id: int = Field(None, description="关联项目id")
    test_user: str = Field(None, description="测试人员")
    leader_user: str = Field(None, description="模块负责人")
    dev_user: str = Field(None, description="开发人员")
    publish_app: str = Field(None, description="发布应用")
    simple_desc: str = Field(None, description="简要描述")
    remarks: str = Field(None, description="备注")
    config_id: int = Field(None, description="关联配置id")
    priority: int = Field(None, description="优先级")


class ModuleQuery(BaseSchema):
    """
    模块查询参数序列化
    """
    id: int = Field(None, description="模块id")
    ids: typing.List = Field(None, description="模块id列表")
    project_ids: typing.List = Field(None, description="项目id列表")
    user_ids: typing.List = Field(None, description="用户id列表")
    name: str = Field(None, description="模块名称")
    project_name: str = Field(None, description="项目名称")
    project_id: int = Field(None, description="项目id")
    order_field: str = Field(None, description="排序字段")
    sort_type: str = Field(None, description="排序方式")
    created_by_name: str = Field(None, description="创建人名称")


class ModuleId(BaseSchema):
    """
    模块id序列化
    """
    id: int = Field(..., description="模块id")
