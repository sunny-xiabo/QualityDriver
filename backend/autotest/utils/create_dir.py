"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: create_dir.py
# @Date: 2023/12/18 17:20
"""
from pathlib import Path  # 导入 Path 类，它提供了一些用于处理文件和文件路径的方法


def create_dir(file_name: str) -> Path:
    """
    创建文件夹
    :param file_name:
    :return: 创建的文件夹的路径
    """
    path = Path(
        file_name).absolute().parent / file_name  # 创建一个 Path 对象，表示 file_name 的绝对路径。然后获取这个路径的父路径，并添加 file_name，得到新的路径
    if not Path(path).exists():  # 检查这个路径是否存在
        Path.mkdir(path) # 如果路径不存在，就创建一个新的文件夹

    return path  # 返回创建的文件夹的路径
