"""
# -*- coding:utf-8 -*-
# @Author: Carl
# @File: main.py
# @Date: 2023/12/11 16:47
"""
import uvicorn
from fastapi import FastAPI
from config import config

# 创建FastAPI应用
app = FastAPI(title="Quality Driver", version=config.PROJECT_VERSION)


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=8101, reload=True)