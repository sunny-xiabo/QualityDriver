"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: api_models.py
# @Date: 2024/1/12 20:49
"""
from sqlalchemy import String, Integer, select, and_
from sqlalchemy.orm import mapped_column, aliased

from autotest.models import Base
from autotest.models.system_models import User
from autotest.schemas.api.project import ProjectQuery


class ProjectInfo(Base):
    """项目表"""

    __tablename__ = 'project_info'

    name = mapped_column(String(64), nullable=False, comment="项目名称", index=True)
    responsible = mapped_column(String(64), nullable=False, comment="负责人")
    test_user = mapped_column(String(100), nullable=False, comment="测试人员")
    dev_user = mapped_column(String(100), nullable=False, comment="开发人员")
    publish_app = mapped_column(String(100), nullable=False, comment="发布应用")
    simple_desc = mapped_column(String(255), nullable=False, comment="简要描述")
    remarks = mapped_column(String(255), comment="备注")
    config_id = mapped_column(Integer, nullable=False, comment="关联配置id")
    product_id = mapped_column(Integer, nullable=False, comment="关联产品id")

    @classmethod
    async def get_list(cls, params: ProjectQuery):
        """
        获取项目列表
        :param params:
        :return:
        """
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.created_by_name:
            q.append(User.nickname.like(f'%{params.created_by_name}%'))
        if params.id:
            q.append(cls.id == params.id)
        if params.ids:
            q.append(cls.id.in_(params.ids))
        u = aliased(User)
        stmt = (select(cls.get_table_columns(),
                       u.nickname.label("updated_by_name"),
                       User.nickname.label("created_by_name"))
                .where(*q)
                .outerjoin(u, u.id == cls.updated_by)
                .outerjoin(User, User.id == cls.created_by)
                .order_by(cls.id.desc()))
        return await cls.pagination(stmt)

    @classmethod
    async def get_project_by_id(cls, id: int):
        """
        获取项目id
        :param id:
        :return:
        """
        stmt = select(cls.get_table_columns()).where(and_(cls.id == id, cls.enabled_flag == 1))
        return await cls.get_result(stmt, True)

    @classmethod
    def get_project_id_list(cls):
        """
        获取项目id列表
        :return:
        """
        return (cls.query.filter(cls.enabled_flag == 1)
                .with_entities(cls.id,
                               cls.responsible,
                               cls.test_user,
                               cls.dev_user,
                               cls.created_by)
                .all())

    @classmethod
    async def get_project_by_name(cls, name):
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt, True)

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_project_ids(cls):
        return cls.query.filter(cls.enabled_flag == 1).with_entities(cls.id).all()

    @classmethod
    def get_project_by_product_id(cls, product_id):
        return cls.query.filter(cls.enabled_flag == 1, cls.product_id == product_id).with_entities(cls.id).all()