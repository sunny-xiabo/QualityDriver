"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: test.py
# @Date: 2023/12/18 14:07
"""

# num_list = [0.8, 1.2, 1.5, 1.4, 1.1]
#
# new_num_list = sorted(num_list, reverse=False)
# len_num_list = len(new_num_list)
# num = len_num_list // 2
# print(new_num_list[num])
import time

from datetime import datetime

timestamp = str(int(time.time()))
print(timestamp)

now = datetime.now()
times = now.strftime("%Y%m%d%H%M%S")
print(times)