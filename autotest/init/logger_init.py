"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: logger_init.py
# @Date: 2023/12/18 17:18
"""
import logging
import os
import sys
from pathlib import Path

from loguru import logger

from autotest.utils.common import get_str_uuid
from autotest.utils.create_dir import create_dir
from autotest.utils.local import g
from config import config
from datetime import datetime


def logger_file() -> str:
    """
    日志文件名称
    :return:
    """
    log_path = create_dir(config.LOGGER_DIR)

    # 获取当前的日期和时间
    now = datetime.now()
    # 格式化日期和时间
    date_str = now.strftime("%Y%m%d%H%M")
    # 拼接文件名
    filename = f"{config.LOGGER_NAME}_{date_str}.log"

    file_list = sorted(Path(log_path).iterdir(), key=os.path.getmtime)
    # 使用 os.path.getmtime 对文件列表进行排序，最旧的文件会在列表的第一个位置

    if len(file_list) > 3:  # 如果文件数量超过3个
        os.remove(file_list[0])

    return os.path.join(log_path, filename)


def correlation_id_filter(record):
    if not g.trace_id:
        g.trace_id = get_str_uuid()
    record['trace_id'] = g.trace_id
    return record


# 定义日志输出的格式
fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
# 移除所有已经添加的日志处理器
logger.remove()
# 添加文件处理器
logger.add(
    logger_file(),  # 输出到文件
    encoding=config.GLOBAL_ENCODING,  # 编码
    level=config.LOGGER_LEVEL,  # 日志级别
    rotation=config.LOGGER_ROTATION,  # 保存策略
    retention=config.LOGGER_RETENTION,  # 保存策略
    filter=correlation_id_filter,  # 过滤器
    format=fmt  # 格式
)
# 添加控制台处理器
logger.add(
    sys.stdout,  # 输出到控制台
    level=config.LOGGER_LEVEL,  # 日志级别
    colorize=True,  # 使用彩色输出
    filter=correlation_id_filter,  # 过滤器
    format=fmt
)


class InterceptHandler(logging.Handler):
    """
    自定义的日志处理器，用于拦截由Python内置的logging模块产生的日志消息，
    并将它们重定向到Loguru的logger对象
    """

    def emit(self, record):
        """
        当一个日志消息需要被处理时，这个方法会被调用。
        :param record:
        :return:
        """
        # 尝试获取体制消息的级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # 创建一个logger选项对象，设置深度为6，异常信息为record.exc_info
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        # 使用logger选项对象记录日志消息
        logger_opt.log(level, record.getMessage())


def init_logger():
    """
    初始化日志
    :return:
    """
    # 获取所有的日志记录器的名称
    logger_name_list = [name for name in logging.root.manager.loggerDict]

    for logger_name in logger_name_list:
        """
            对每一个日志记录器，检查它的有效级别是否低于配置文件中指定的日志级别。
            如果是，就设置日志记录器的级别为配置文件中指定的级别
        """
        effect_level = logging.getLogger(logger_name).getEffectiveLevel()
        if effect_level < logging.getLevelName(config.LOGGER_LEVEL.upper()):
            logging.getLogger(logger_name).setLevel(config.LOGGER_LEVEL.upper())
        """
                如果日志记录器的名称中包含 "."，就清空日志记录器的处理器列表，
                并添加一个 InterceptHandler 对象作为新的处理器。
        """
        if "." in logger_name:
            logging.getLogger(logger_name).handlers = []
            logging.getLogger(logger_name).addHandler(InterceptHandler())
