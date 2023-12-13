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
