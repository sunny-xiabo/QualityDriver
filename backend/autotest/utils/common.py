"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: common.py
# @Date: 2023/12/16 20:13
"""
import uuid


def get_str_uuid():
    return str(uuid.uuid4()).replace("-", "")
