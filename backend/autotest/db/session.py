"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: session.py
# @Date: 2023/12/12 18:39
"""
import functools
import traceback
import typing
from asyncio import current_task

from loguru import logger
from sqlalchemy import create_engine

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import sessionmaker

from autotest.utils.local import g
from config import config


# 创建表引擎


async_engine = create_async_engine(
    url=config.DATABASE_URI,  # 数据库uri
    echo=config.DATABASE_ECHO,  # 是否打印日志
    pool_size=10,  # 队列池个数
    max_overflow=20,  # 队列池最大溢出个数
    pool_pre_ping=True,  # 将启用连接池“预ping”功能，该功能在每次签出时测试连接的活跃度
    pool_recycle=7200,  # 2个小时回收线程
)

# 操作表会话
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False  # 防止提交后属性过期
)

# 创建异步的会话作用域
"""
sync_scoped_session 函数创建一个新的 ScopedSession 对象，它是一个可以生成新的 Session 对象的工厂，同时也确保所有的会话都在同一线程中被
正确地处理。

这里的 async_session_factory 是一个函数，它应该返回一个新的 Session 对象。scopefunc 参数是一个函数，它决定了当前会话的作用域。在这个例
子中，scopefunc 被设置为 current_task，这意味着每个 asyncio 任务都有自己的会话。
"""
async_session = async_scoped_session(async_session_factory, scopefunc=current_task)


sync_engine = create_engine(
    url=config.DATABASE_URI,  # 数据库uri
    echo=config.DATABASE_ECHO,  # 是否打印日志
    pool_size=10,  # 队列池个数
    max_overflow=20,  # 队列池最大溢出个数
    pool_pre_ping=True,  # 将启用连接池“预ping”功能，该功能在每次签出时测试连接的活跃度
    pool_recycle=7200,  # 2个小时回收线程
)
sync_session = sessionmaker(bind=sync_engine, autoflush=False, autocommit=False, expire_on_commit=False)


def provide_async_session(func: typing.Callable):
    """
    单事务回滚
    装饰器函数 provide_async_session 接收一个函数 func 作为参数。这个函数应该是一个异步函数，它可能需要一个 SQLAlchemy 的异步会话来执
    行数据库操作。

    装饰器函数返回一个新的异步函数 wrapper。这个函数在被调用时会检查原函数 func 的参数中是否已经包含了名为 session 的参数。如果已经包含了
     session 参数，那么 wrapper 函数会直接调用 func 函数并返回结果。

    如果 func 函数的参数中没有 session 参数，那么 wrapper 函数会创建一个新的异步会话，并将这个会话作为关键字参数传递给 func 函数。在调用
    func 函数之前，wrapper 函数会开始一个新的事务。

    wrapper 函数使用 try/except 块来处理可能发生的异常。如果 func 函数执行成功，那么 wrapper 函数会提交事务并返回 func 函数的结果。如果
     func 函数抛出了 IntegrityError 异常或其他任何异常，那么 wrapper 函数会回滚事务并重新抛出这个异常。
    :param func: 函数
    :return:
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        arg_session = 'session'

        func_params = func.__code__.co_varnames
        session_in_args = arg_session in func_params and func_params.index(arg_session) < len(args)
        session_in_kwargs = arg_session in kwargs

        if session_in_kwargs or session_in_args:
            return await func(*args, **kwargs)
        else:
            async with async_session() as session:
                try:
                    result = await func(session=session, *args, **kwargs)
                    await session.commit()
                    return result
                except IntegrityError:
                    logger.error(traceback.format_exc())
                    await session.rollback()
                    raise
                except Exception:
                    logger.error(traceback.format_exc())
                    await session.rollback()
                    raise

    return wrapper


def provide_async_session_router(func: typing.Callable):
    """
    路由全局错误回滚
    :param func: 函数
    :return:
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            g.zero_db_session = session
            try:
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                logger.error(traceback.format_exc())
                raise
            except Exception:
                await session.rollback()
                logger.error(traceback.format_exc())
                raise
    return wrapper

