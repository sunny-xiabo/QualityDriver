"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: role.py
# @Date: 2024/1/2 20:52
"""

from fastapi import APIRouter

from autotest.schemas.system.roles import RoleQuery, RoleInfo, RoleDel
from autotest.services.system.role import RoleService
from autotest.utils.response_http_response import partner_success

router = APIRouter()

@router.post("/list", description="获取角色列表")
async def all_roles(params:RoleQuery):
    """
    获取角色列表
    :param params:
    :return:
    """
    data = await RoleService.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存或更新角色")
async def save_or_update_role(params:RoleInfo):
    """
    保存或更新角色
    :param params:
    :return:
    """
    try:
        data = await RoleService.save_or_update(params)
        return partner_success(data)
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)

@router.post("/deleted", description="删除角色")
async def deleted(params:RoleDel):
    """
    删除角色
    :param params:
    :return:
    """
    try:
        data = await RoleService.deleted(params)
        return partner_success(data)
    except ValueError as e:
        code, msg = e.args
        return partner_success(code=code, msg=msg)