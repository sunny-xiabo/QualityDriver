"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: base.py
# @Date: 2023/12/12 10:29
"""

import typing
from math import ceil

from sqlalchemy import BigInteger, DateTime, func, Boolean, String, select, Executable, Result, ClauseList, Select, \
    insert, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import mapped_column
from autotest.utils.current_user import current_user

from autotest.db.session import provide_async_session
from autotest.exceptions.exceptions import AccessTokenFail
from autotest.utils.consts import DEFAULT_PAGE, DEFAULT_PER_PAGE
from autotest.utils.local import g
from autotest.utils.serialize import unwrap_scalars, count_query, paginate_query


@as_declarative()
class Base:
    """
    基础表
    """

    __name__: str  # 表名

    __table_args__ = {
        'mysql_charset': 'utf8'}  # 设置表字符集
    __mapper_args__ = {
        'eager_defaults': True}  # 防止 insert 时不刷新

    id = mapped_column(BigInteger(), nullable=False, primary_key=True, autoincrement=True, comment="主键")
    creation_date = mapped_column(DateTime(), default=func.now(), comment="创建时间")
    created_by = mapped_column(BigInteger, comment='创建人ID')
    updating_date = mapped_column(DateTime(), default=func.now(), onupdate=func.now(), comment='更新时间')
    updated_by = mapped_column(BigInteger, comment='更新人ID')
    enabled_flag = mapped_column(Boolean(), default=1, nullable=False, comment='是否删除, 0 删除 1 非删除')
    trace_id = mapped_column(String(255), comment="trace_id")

    @classmethod
    async def get(cls, id: typing.Union[int, str], to_dict: object = False, include_deleted: bool = False) -> \
    typing.Union["Base", typing.Dict, None]:
        """
        封装查询
        :param id: 查询id
        :param to_dict: 转换为字典
        :param include_deleted: 是否包含已删除的记录
        :return: 模型对象
        """
        if not id:
            return None
        if include_deleted:
            sql = select(cls).where(cls.id == id)
        else:
            sql = select(cls).where(and_(cls.id == id, cls.enabled_flag == 1))  # enabled_flag是软删除字段，默认为1
        result = await cls.execute(sql)
        data = result.scalars().first()
        return data if not to_dict else unwrap_scalars(data)

    @classmethod
    async def get_all(cls) -> typing.Optional[typing.Any]:
        """
        获取所有
        :return: 返回所有数据 list[dict]
        """
        stmt = select(cls.get_table_columns()).where(cls.enabled_flag == 1)
        return await cls.get_result(stmt)

    @classmethod
    async def create_or_update(cls, params: typing.Union[typing.Dict]) -> typing.Dict[typing.Text, typing.Any]:
        """
        创建或更新
        :param params: 更新数据 dict
        :return: 更新后的数据 dict
        """
        if not isinstance(params, dict):
            raise ValueError("更新参数错误！")
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        id = params.get("id", None)
        params = await cls.handle_params(params)
        exist_data = await cls.get(id)
        if exist_data:
            stmt = update(cls).where(cls.id == id).values(**params)
        else:
            stmt = insert(cls).values(**params)
        result = await cls.execute(stmt)
        if result.is_insert:
            (primary_key,) = result.inserted_primary_key
            params["id"] = primary_key
        return params

    @classmethod
    async def create(cls, params: typing.Dict, to_dict: bool = False) -> typing.Union["Base", typing.Dict]:
        """
        插入数据
        :param params: 批量插入数据
        :param to_dict: 是否转字典
        :return: 插入数量
        """
        if not isinstance(params, dict):
            raise ValueError("参数错误")
        params = {key: value for key, value in params.items() if hasattr(cls, key)}
        params = await cls.handle_params(params)
        stmt = insert(cls).values(**params)
        result = await cls.execute(stmt)
        (primary_key,) = result.inserted_primary_key
        params["id"] = primary_key
        return cls(**params) if not to_dict else params

    @classmethod
    async def batch_create(cls, params: typing.List) -> int:
        """
        批量插入数据
        :param params: 批量插入数据
        :return: 插入数量
        """
        if not isinstance(params, list):
            raise ValueError("参数错误，参数必须为列表")
        params = await cls.handle_params(params)
        stmt = insert(cls).values(params)
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def handle_params(cls, params: typing.Any) -> typing.Any:
        """
        :param params: 参数列表
        :return: 过滤好的参数
        """
        if isinstance(params, dict):
            params = cls.filter_params(params)
            params = await cls.update_params(params)
        elif isinstance(params, list):
            params = [await cls.handle_params(p) for p in params]
        return params

    @classmethod
    async def delete(cls, id: typing.Union[int, str], _hard: bool = False) -> int:
        """
        删除
        :param id: 删除id
        :return:
        """
        if _hard is False:
            stmt = update(cls).where(cls.id == id, cls.enabled_flag == 1).values(enabled_flag=0)
        else:
            stmt = delete(cls).where(cls.id == id)
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def execute(cls, stmt: Executable, params: typing.Any = None) -> Result[typing.Any]:
        """
        执行
        :param stmt: sqlalchemy Executable 对象
        :param params: params参数
        :return:
        """
        session = g.qd_db_session
        if session:
            return await session.execute(stmt, params)
        return await cls.execute_by_session(stmt, params)

    @classmethod
    @provide_async_session
    async def execute_by_session(cls, stmt: Executable, params: typing.Any = None, session: AsyncSession = None) -> \
        Result[typing.Any]:
        """
        session 执行
        :param stmt: sqlalchemy Executable 对象
        :param params: params 参数
        :param session: session db会话
        :return:
        """
        return await session.execute(stmt, params)

    @classmethod
    async def execute_by_local(cls, stmt: Executable, params: typing.Any = None) -> Result[typing.Any]:
        """
        执行sql
        :param stmt: sqlalchemy Executable 对象
        :param params: params 参数
        :return:
        """
        session = g.db_session
        return await session.execute(stmt, params)

    @classmethod
    async def pagination(cls, stmt: Select) -> typing.Dict[str, typing.Any]:
        """
        分页查询
        :param stmt: select对象
        :return:
        """
        return await parse_pagination(stmt)

    @classmethod
    def get_table_columns(cls, exclude: set = None) -> ClauseList:
        """
        获取模型所有字段
        exclude: 排除字段  {"name"}
        :return:
        """
        exclude = exclude if exclude else set()
        return ClauseList(*[i for i in cls.__table__.columns if i.name not in exclude])

    @classmethod
    async def get_result(cls, stmt: Select, first=False) -> typing.Any:
        """
        获取查询结果转为dict
        first=True：
        {
            "key": "value"
            ...
        }
        first=False：
        [
            {
                "key1": "value1"
                ...
            },
            {
                "key2": "value2"
                ...
            }
        ]
        :param stmt:
        :param first:
        :return:
        """
        result = await cls.execute(stmt)
        data = result.first() if first else result.fetchall()
        return unwrap_scalars(data) if data else None

    @classmethod
    async def filter_params(cls, params: dict) -> dict:
        """过滤参数，只保留类属性"""
        return {key: value for key, value in params.items() if hasattr(cls, key)}

    @classmethod
    async def update_params(cls, params: dict) -> dict:
        """更新参数，添加或更新 trace_id、updated_by 和 created_by"""
        params = await params
        params['trace_id'] = g.trace_id
        try:
            current_user_info = await current_user()
        except AccessTokenFail:
            current_user_info = None
        if current_user_info:
            current_user_id = current_user_info.get("id", None)
            params["updated_by"] = current_user_id
            if not params.get("id", None):
                params["created_by"] = current_user_id
        else:
            params["updated_by"] = params.get("updated_by", 0)
            params["created_by"] = params.get("created_by", 0)
        return params


@provide_async_session
async def parse_pagination(
    query: select,
    page: int = None,
    page_size: int = None,
    session: AsyncSession = None) -> typing.Dict[str, typing.Any]:
    """
    异步处理分页查询的结果。

    :param query: SQLAlchemy 查询对象。
    :param page: 页码，默认为 None。如果没有提供，将从请求中获取。
    :param page_size: 页面大小，默认为 None。如果没有提供，将从请求中获取。页面大小最大为 1000。
    :param session: SQLAlchemy 异步会话对象。

    :return: 一个字典，包含以下键：
        'rowTotal': 查询结果的总行数。
        'pageSize': 页面大小。
        'page': 当前页码。
        'pageTotal': 总页数。
        'rows': 查询结果，作为一个列表返回。

    如果请求方法是 POST，页码和页面大小将从请求的 JSON 数据中获取。
    否则，它们将从请求的参数中获取。

    查询结果将使用 `unwrap_scalars` 函数进行处理，以便将 SQLAlchemy 的 `Row` 对象转换为 Python 的字典。
    """
    if g.request.method == 'POST':
        request_json = await g.request.json()
        page = int(request_json.get('page', DEFAULT_PAGE)) if not page else page
        page_size = min(int(request_json.get('pageSize', DEFAULT_PER_PAGE)),
                        1000) if not page_size else page_size
    else:
        page = g.request.args.get('page', type=int, default=DEFAULT_PAGE) if not page else page
        page_size = min(g.request.args.get('pageSize', type=int, default=DEFAULT_PER_PAGE),
                        1000) if not page_size else page_size
    (total,) = (await session.execute(count_query(query))).scalars()
    result = (await session.execute(paginate_query(query, page=page, page_size=page_size))).fetchall()
    result = unwrap_scalars(result)
    total_page = int(ceil(float(total) / page_size))
    pagination = {
        'rowTotal': total,
        'pageSize': page_size,
        'page': page,
        'pageTotal': total_page,
        'rows': result,
    }

    return pagination
