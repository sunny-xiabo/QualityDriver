"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: api_models.py
# @Date: 2024/1/12 20:49
"""
from sqlalchemy import String, Integer, select, and_, func, distinct, text, BigInteger, JSON, Text
from sqlalchemy.orm import mapped_column, aliased

from autotest.models import Base
from autotest.models.system_models import User
from autotest.schemas.api.module import ModuleQuery
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


class ModuleInfo(Base):
    """
    模块表
    """
    __tablename__ = 'module_info'

    name = mapped_column(String(64), nullable=False, comment="模块名称", index=True)
    project_id = mapped_column(Integer, nullable=False, comment="关联项目id")
    config_id = mapped_column(Integer, nullable=False, comment="关联配置id")
    test_user = mapped_column(String(100), nullable=False, comment="测试人员")
    simple_desc = mapped_column(String(255), nullable=False, comment="简要描述")
    remarks = mapped_column(String(255), comment="备注")
    module_packages = mapped_column(String(255), comment="模块包名")
    leader_user = mapped_column(String(64), nullable=False, comment="模块负责人")
    priority = mapped_column(Integer, comment="执行用例优先级", default=4)

    @classmethod
    async def get_list(cls, params: ModuleQuery):
        """
        获取模块列表
        :param params:
        :return:
        """
        # 初始化查询条件列表
        conditions = [cls.enabled_flag == 1]
        # 根据参数添加查询条件
        if params.name:
            conditions.append(cls.name.like(f'%{params.name}%'))
        if params.project_id:
            conditions.append(cls.project_id == params.project_id)
        if params.project_name:
            conditions.append(ProjectInfo.name.like(f'%{params.project_name}%'))
        if params.user_ids:
            conditions.append(cls.created_by.in_(params.user_ids))
        if params.project_ids:
            conditions.append(cls.project_id.in_(params.project_ids))
        if params.ids:
            conditions.append(cls.id.in_(params.ids))
        # 设置排序方式
        sort_type = 'asc' if params.sort_type == 0 else 'desc'
        # 迎神排序字段到数据库字段
        order_field_mapping = {
            'creation_date': 'module_info.creation_date',
            'project_name': 'project_info.name',
            'test_user': 'user.nickname'
        }
        # 获取排序字段
        params.order_field = order_field_mapping.get(params.order_field, params.order_field)
        # 构造排序字符串
        order_by = f'{params.order_field} {sort_type}, module_info.id {sort_type}'
        # 创建别名方便在查询中使用
        updated_by_alias = aliased(User)

        # 构造查询语句
        stmt = select(cls.get_table_columns(),
                      func.count(distinct(ApiInfo.id)).label('case_count'),
                      User.nickname.label('created_by_name'),
                      updated_by_alias.nickname.label('updated_by_name'),
                      ProjectInfo.name.label('project_name')).where(*conditions) \
            .outerjoin(ProjectInfo, and_(cls.project_id == ProjectInfo.id, ProjectInfo.enabled_flag == 1)) \
            .outerjoin(User, User.id == cls.created_by) \
            .outerjoin(updated_by_alias, updated_by_alias.id == cls.updated_by) \
            .outerjoin(ApiInfo, and_(cls.id == ApiInfo.module_id, ApiInfo.enabled_flag == 1)) \
            .group_by(cls.id).order_by(text(order_by))
        # 执行查询并返回结果
        return await cls.pagination(stmt)

    @classmethod
    async def get_module_by_project_id(cls, project_id: int):
        """
        查询项目是否关联模块
        """
        stmt = select(cls.id).where(cls.project_id == project_id, cls.enabled_flag == 1)
        return await cls.get_result(stmt)


    @classmethod
    async def get_module_by_name(cls, name: str):
        """
        查询模块名称
        """
        stmt = select(cls.id).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def get_module_by_id(cls, module_packages):
        """
        查询模块id
        """
        return cls.query.filter(cls.module_packages == module_packages, cls.enabled_flag == 1).all()

    @classmethod
    def get_all_count(cls):
        return cls.query.filter(cls.enabled_flag == 1).count()

    @classmethod
    def get_module_by_packages_id(cls, packages_id):
        return cls.query.filter(cls.packages_id == packages_id, cls.enabled_flag == 1).first()


class ApiInfo(Base):
    """
    接口表
    """
    __tablename__ = 'api_info'

    name = mapped_column(String(255), nullable=False, comment="接口名称", index=True)
    project_id = mapped_column(BigInteger, nullable=False, comment="所属项目")
    module_id = mapped_column(BigInteger, nullable=False, comment="所属模块")
    status = mapped_column(Integer, comment="接口状态 10 生效， 20 失败", default=10)
    code_id = mapped_column(BigInteger, nullable=False, comment="关联接口id")
    code = mapped_column(String(255), comment='接口code')
    priority = mapped_column(Integer, comment="执行用例优先级", default=3)
    tags = mapped_column(JSON, comment="接口标签")
    url = mapped_column(String(255), nullable=False, comment="接口地址")
    method = mapped_column(String(255), comment="请求方式")
    remarks = mapped_column(String(255), comment="接口描述")
    step_type = mapped_column(String(255), comment="步骤类型")
    pre_steps = mapped_column(JSON, comment="前置步骤")
    post_steps = mapped_column(JSON, comment="后置步骤")
    setup_code = mapped_column(Text, comment="前置代码")
    teardown_code = mapped_column(Text, comment="后置代码")
    setup_hooks = mapped_column(JSON, comment="前置钩子")
    teardown_hooks = mapped_column(JSON, comment="后置钩子")
    headers = mapped_column(JSON, comment="请求头")
    request = mapped_column(JSON, comment="请求参数")
    variables = mapped_column(JSON, comment="变量")
    validators = mapped_column(JSON, comment="断言")
    extracts = mapped_column(JSON, comment="提取")
    export = mapped_column(JSON, comment="输出")
