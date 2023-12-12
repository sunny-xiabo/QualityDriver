"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: local.py
# @Date: 2023/12/12 14:01
"""

from contextvars import ContextVar
import typing


class Local:
    """
    提供一个本地存储，可以在其中存储和检索值，同时这些值对于每个上下文（例如，每个线程或异步任务）都是独立的

    ContextVar 是 Python 3.7 引入的一个新特性，它用于管理上下文本地状态。这是一种在异步编程中非常有用的工具，因为它允许你在每个上下文
    （例如，每个线程或异步任务）中存储和检索独立的值。

    ContextVar 的一个常见用途是跟踪当前执行的任务或请求。例如，你可能想要在处理 HTTP 请求时存储一些信息，如请求 ID 或用户身份，然后在
    处理该请求的整个生命周期中访问这些信息。使用 ContextVar，你可以在每个请求的上下文中存储这些信息，而不必担心它们会被其他请求的信息覆盖。
    """
    __slots__ = ("_storage",)  # 优化内存使用，表示 Local 类的实例只能有一个名为 _storage 的属性

    def __init__(self) -> None:
        """
        初始化
        """
        object.__setattr__(self, "_storage", ContextVar("local_storage"))

    def __iter__(self) -> typing.Iterator[typing.Tuple[int, typing.Any]]:
        """
        迭代
        """
        return iter(self._storage.get({}).items())

    def __release_local__(self) -> None:
        """
        释放
        """
        self._storage.set({})

    def __getattr__(self, name: str) -> typing.Any:
        """
        获取属性
        """
        values = self._storage.get({})
        try:
            return values[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        设置属性
        """
        values = self._storage.get({}).copy()
        values[name] = value
        self._storage.set(values)

    def __delattr__(self, name: str) -> None:
        """
        删除属性
        :param name:
        :return:
        """
        values = self._storage.get({}).copy()
        try:
            del values[name]
            self._storage.set(values)
        except KeyError:
            ...

g = Local()

