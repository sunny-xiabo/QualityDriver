"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: serialize.py
# @Date: 2023/12/12 15:28
"""
from datetime import datetime
import typing
from json import JSONEncoder

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Select, Row, select, func, literal_column
from sqlalchemy.orm import DeclarativeMeta, noload

T = typing.TypeVar("T", Select, "Query[Any]")


def count_query(query: Select) -> Select:
    """
    获取count sql
    :param query: sql
    :return:
    """
    count_subquery = typing.cast(typing.Any, query.order_by(None)).options(noload("*")).subquery()
    return select(func.count(literal_column("*"))).select_from(count_subquery)


def paginate_query(query: T, page: int, page_size: int) -> T:
    """
    获取分页sql
    :param query:
    :param page: 页数
    :param page_size: 每页大小
    :return:
    """
    return query.limit(page_size).offset(page_size * (page - 1))


def len_or_none(obj: typing.Any) -> typing.Optional[int]:
    """有数据返回长度 没数据返回None"""
    try:
        return len(obj)
    except TypeError:
        return None


def unwrap_scalars(items: typing.Union[typing.Sequence[Row], Row]) -> typing.Union[
    typing.List[typing.Dict[typing.Text, typing.Any]], typing.Dict[str, typing.Any]]:
    """
    将数据库查询Row结果转换为字典
    :param items:
    :return:
    """
    if isinstance(items, typing.Iterable) and not isinstance(items, Row):
        return [default_serialize(item) for item in items]
    return default_serialize(items)


class MyJsonDecode(JSONEncoder):
    """
    自定义序列化
    """

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return default_serialize(obj)


def serialize_dict_or_row(obj):
    """
    序列化字典或列
    :param obj:
    :return:
    """
    if isinstance(obj, Row):
        obj = dict(zip(obj._fields, obj._data))
    return {key: default_serialize(value) for key, value in obj.items()}


def serialize_general(obj):
    if hasattr(obj, "__class__") and isinstance(obj.__class__, DeclarativeMeta):
        return {c.name: default_serialize(getattr(obj, c.name)) for c in obj.__table__.columns}
    try:
        return jsonable_encoder(obj)
    except TypeError:
        return repr(obj)


def default_serialize(obj):
    """默认序列化"""
    try:
        if isinstance(obj, int) and len(str(obj)) > 15:
            return str(obj)
        if isinstance(obj, (dict, Row)):
            return serialize_dict_or_row(obj)
        if isinstance(obj, list):
            return [default_serialize(i) for i in obj]
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, typing.Callable):
            return repr(obj)
        return serialize_general(obj)
    except TypeError as err:
        return repr(obj)
