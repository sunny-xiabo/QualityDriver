"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: role.py
# @Date: 2024/1/2 20:30
"""
import traceback
import typing

from loguru import logger

from autotest.models.system_models import Roles, User
from autotest.schemas.system.roles import RoleQuery, RoleInfo, RoleDel
from autotest.utils.response_http_response import CodeEnum


class RoleService:
    """
    角色服务
    """

    @staticmethod
    async def list(params: RoleQuery) -> typing.Dict[str, typing.Any]:
        """
        获取角色列表
        :param params:
        :return:
        """
        data = await Roles.get_list(params)
        for row in data.get("rows", []):
            row["menus"] = list(map(int, (row["menus"].split(",")))) if row["menus"] else []
        return data

    @staticmethod
    async def save_or_update(params: RoleInfo) -> int:
        """
        保存或更新角色
        :param params:
        :return:
        """
        # 如果角色ID存在，获取角色信息
        if params.id:
            role_info = await Roles.get(params.id)
            # 如果数据库中没有这个ID，抛出一个错误
            if role_info is None:
                raise ValueError(CodeEnum.ROLE_ID_IS_NOT_EXIST.code,
                                 CodeEnum.ROLE_ID_IS_NOT_EXIST.msg)
            # 如果角色名已经改变，并且新的角色名已经存在，那么抛出一个错误
            if role_info.name != params.name:
                if await Roles.get_roles_by_name(params.name):
                    raise ValueError(CodeEnum.ROLE_NAME_IS_EXIST.code,
                                     CodeEnum.ROLE_NAME_IS_EXIST.msg)
        # 如果角色ID不存在，直接检查新的角色名是否已经存在
        elif await Roles.get_roles_by_name(params.name):
            raise ValueError(CodeEnum.ROLE_NAME_IS_EXIST.code,
                             CodeEnum.ROLE_NAME_IS_EXIST.msg)

        # 保存或更新角色信息
        result = await Roles.create_or_update(params.dict())
        return result

    @staticmethod
    async def deleted(params: RoleDel) -> int:
        """
        删除角色
        :param params:
        :return:
        """
        try:
            # 获取角色信息
            role_info = await Roles.get(params.id, include_deleted=True)
            # 如果数据库中没有这个ID，抛出一个错误
            if role_info is None:
                raise ValueError(CodeEnum.ROLE_ID_IS_NOT_EXIST.code,
                                 CodeEnum.ROLE_ID_IS_NOT_EXIST.msg)
            # 如果角色已经被软删除，抛出一个错误
            elif role_info.enabled_flag == False:
                raise ValueError(CodeEnum.ROLE_IS_DISABLE.code,
                                 CodeEnum.ROLE_IS_DISABLE.msg)
            # 如果角色不存在，抛出一个错误
            relation_data = await User.get_user_by_roles(params.id)
            if relation_data:
                raise ValueError(CodeEnum.ROLE_ASSOCIATED_USER.code,
                                 CodeEnum.ROLE_ASSOCIATED_USER.msg)
            return await Roles.delete(params.id)
        except Exception as e:
            logger.error(traceback.format_exc())
