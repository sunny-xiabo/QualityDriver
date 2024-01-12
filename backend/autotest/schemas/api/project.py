"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: project.py
# @Date: 2024/1/12 21:04
"""
import typing

from pydantic import BaseModel, Field

from autotest.schemas.base import BaseSchema


class ProjectInfo(BaseModel):
    """项目信息序列化"""
    id: int = Field(None, description="项目id")
    name: str = Field(..., description="项目名称")
    test_user: str = Field(None, description="测试人员")
    dev_user: str = Field(None, description="开发人员")
    publish_app: str = Field(None, description="发布应用")
    responsible: str = Field(None, description="负责人")
    simple_desc: str = Field(None, description="简要描述")
    remarks: str = Field(None, description="备注")
    config_id: int = Field(None, description="关联配置id")


class ProjectQuery(BaseSchema):
    """
    项目查询参数序列化
    """
    id: int = Field(None, description="项目id")
    ids: typing.List = Field(None, description="项目id列表")
    name: str = Field(None, description="项目名称")
    order_field: str = Field(None, description="排序字段")
    order_type: str = Field(None, description="排序方式")
    created_by_name: str = Field(None, description="创建人")

class ProjectDel(BaseSchema):
    """
    项目删除参数序列化
    """
    id: int = Field(..., description="项目id")
