"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: config.py
# @Date: 2023/12/11 16:53
"""
import os.path
import typing

from pydantic import BaseSettings, AnyHttpUrl, Field

project_logo = """
   ███████                       ██ ██   ██            ███████          ██                        
  ██░░░░░██                     ░██░░   ░██    ██   ██░██░░░░██        ░░                         
 ██     ░░██  ██   ██  ██████   ░██ ██ ██████ ░░██ ██ ░██    ░██ ██████ ██ ██    ██  █████  ██████
░██      ░██ ░██  ░██ ░░░░░░██  ░██░██░░░██░   ░░███  ░██    ░██░░██░░█░██░██   ░██ ██░░░██░░██░░█
░██    ██░██ ░██  ░██  ███████  ░██░██  ░██     ░██   ░██    ░██ ░██ ░ ░██░░██ ░██ ░███████ ░██ ░ 
░░██  ░░ ██  ░██  ░██ ██░░░░██  ░██░██  ░██     ██    ░██    ██  ░██   ░██ ░░████  ░██░░░░  ░██   
 ░░███████ ██░░██████░░████████ ███░██  ░░██   ██     ░███████  ░███   ░██  ░░██   ░░██████░███   
  ░░░░░░░ ░░  ░░░░░░  ░░░░░░░░ ░░░ ░░    ░░   ░░      ░░░░░░░   ░░░    ░░    ░░     ░░░░░░ ░░░    

"""

__version__ = "0.0.1"


class Configs(BaseSettings):
    """
    全局配置
    """
    PROJECT_LOGO: str = project_logo  # 项目logo
    PROJECT_NAME: str = "Quality Driver"  # 项目名称
    PROJECT_VERSION: typing.Union[str, int] = __version__  # 项目版本
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8100"  # 基础URL

    # 文件目录
    BASEDIR: str = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

    API_PREFIX: str = "/api"  # 接口前缀
    GLOBAL_ENCODING: str = "utf-8"  # 全局编码


    # 数据库配置
    DATABASE_URI: str = Field(..., env="MYSQL_DATABASE_URI")
    DATABASE_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)

    # redis
    REDIS_URI: str = Field(..., env="REDIS_URI")

    class Config:
        case_sensitive = True  # 区分大小写
        env_file = ".env.example"  # 指定环境变量文件的路径
        env_file_encoding = "utf-8"  # 指定环境变量文件的编码


config = Configs()
