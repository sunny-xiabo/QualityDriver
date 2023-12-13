"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: __init__.py.py
# @Date: 2023/12/12 10:26
"""
from autotest.db.session import async_engine
from autotest.models.base import Base

async def init_db():
    """
    初始化数据库
    :return:
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)