"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: system_models.py
# @Date: 2023/12/12 10:27
"""

import typing

from sqlalchemy import String, Text, JSON, Integer, select, and_
from sqlalchemy.orm import mapped_column, aliased

from autotest.models.base import Base
from autotest.schemas.system.roles import RoleQuery
from autotest.schemas.system.user import UserQuery


class User(Base):
    """
    用户表
    """
    __tablename__ = "user"

    username = mapped_column(String(64), nullable=False, comment="用户名", index=True)
    password = mapped_column(Text, nullable=False, comment="密码")
    email = mapped_column(String(64), comment="邮箱")
    roles = mapped_column(JSON, comment="角色类型")
    status = mapped_column(Integer, comment="用户状态 0-正常 1-禁用", default=0)
    nickname = mapped_column(String(255), comment="昵称")
    user_type = mapped_column(Integer, comment="用户类型 0-普通用户 1-管理员", default=0)
    remarks = mapped_column(Text, comment="备注")
    avatar = mapped_column(Text, comment="头像")
    tags = mapped_column(JSON, comment="标签")

    @classmethod
    async def get_list(cls, params: UserQuery):
        """
        获取用户列表
        :param params:
        :return:
        """
        q = [cls.enabled_flag == 1]  # 初始化一个查询条件列表,并添加了第一个查询条件,即启用的用户
        if params.username:
            q.append(cls.username.like("%{}%".format(params.username)))
        if params.nickname:
            q.append(cls.nickname.like("%{}%".format(params.nickname)))
        if params.user_ids and isinstance(params.user_ids, list):
            q.append(cls.id.in_(params.user_ids))

        u = aliased(User)
        stmt = select(*cls.get_table_columns(), u.nickname.label("created_by_name")). \
            where(*q). \
            outerjoin(u, u.id == cls.created_by) \
            .oder_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_user_by_roles(cls, roles_id: int) -> typing.Any:
        """
        获取用户权限
        :param roles_id:
        :return:
        """
        stmt = select(cls.id).where(cls.roles.like(f"{roles_id}%"), cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_name(cls, username: str):
        """
        获取用户名字
        :param username:
        :return:
        """
        stmt = select(*cls.get_table_columns()).where(cls.username == username, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    async def get_user_by_nickname(cls, nickname: str):
        """
        获取用户昵称
        :param nickname:
        :return:
        """
        stmt = select(*cls.get_table_columns()).where(cls.nickname == nickname, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)


class Roles(Base):
    """
    角色表
    """
    __tablename__ = "roles"

    name = mapped_column(String(64), nullable=False, comment="角色名称", index=True)
    role_type = mapped_column(Integer, comment="角色类型 10-菜单权限 20-用户组权限", default=10)
    menus = mapped_column(String(255), comment="菜单权限", index=True)
    description = mapped_column(Text, comment="描述")
    status = mapped_column(Integer, comment="角色状态 0-正常 1-禁用", default=0)

    @classmethod
    async def get_list(cls, params: RoleQuery):
        # 验证参数
        assert isinstance(params, RoleQuery), "参数错误"

        q = [cls.enabled_flag == 1]
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        q.append(cls.role_type == (params.role_type if params.role_type else 10))

        # 构建查询
        u = aliased(User)
        stmt = (
            select(
                cls.get_table_columns(),
                u.nickname.label("created_by_name"),
                User.nickname.label("updated_by_name")
            )
            .where(*q)
            .outerjoin(u, u.id == cls.created_by)
            .outerjoin(User, User.id == cls.updated_by)
            .order_by(cls.id.desc())
        )

        # 执行查询并返回结果
        return await cls.pagination(stmt)

    @classmethod
    async def get_roles_by_ids(cls,ids: typing.List, role_type=None):
        """
        获取角色
        :param ids:
        :param role_type:
        :return:
        """
        q = [cls.enabled_flag == 1, cls.id.in_(ids)]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    def get_all(cls, role_type=10):
        q= list()
        if role_type:
            q.append(cls.role_type == role_type)
        return cls.query.filter(*q, cls.enabled_flag == 1).order_by(cls.id.desc())

    @classmethod
    async def get_roles_by_name(cls,name,role_type=None):
        q = [cls.enabled_flag == 1, cls.name == name]
        if role_type:
            q.append(cls.role_type == role_type)
        else:
            q.append(cls.role_type == 10)
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt, True)