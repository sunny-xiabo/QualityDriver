"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: project.py
# @Date: 2024/1/12 21:15
"""
import typing

from autotest.models.api_models import ProjectInfo
from autotest.schemas.api.project import ProjectQuery, ProjectDel
from autotest.utils.response_code import CodeEnum


class ProjectService:
    """
    项目服务
    """

    @staticmethod
    async def list(params: ProjectQuery) -> typing.Dict[str, typing.Any]:
        """
        获取项目列表
        :param params:
        :return:
        """
        data = await ProjectInfo.get_list(params)
        return data

    @staticmethod
    async def get_all() -> typing.Dict[str, typing.Any]:
        """
        获取所有项目
        :return:
        """
        data = await ProjectInfo.get_all()
        return data

    @staticmethod
    async def save_or_update(params: ProjectInfo) -> typing.Dict:
        """
        保存或更新项目
        :param params:
        :return:
        """
        # 如果项目id存在，获取项目信息
        if params.id:
            project_info = await ProjectInfo.get(params.id)
            # 如果数据库中没有这个ID，抛出一个错误
            if project_info is None:
                raise ValueError(CodeEnum.PROJECT_ID_IS_NOT_EXIST.code,
                                 CodeEnum.PROJECT_ID_IS_NOT_EXIST.msg)
            # 如果项目名已经改变，并且新的项目名已经存在，那么抛出一个错误
            if project_info.name != params.name:
                if await ProjectInfo.get_project_by_name(params.name):
                    raise ValueError(CodeEnum.PROJECT_NAME_EXIST.code,
                                     CodeEnum.PROJECT_NAME_EXIST.msg)
            # 如果项目id不存在，直接检查新的项目名是否已经存在
            elif await ProjectInfo.get_project_by_name(params.name):
                raise ValueError(CodeEnum.PROJECT_NAME_EXIST.code,
                                 CodeEnum.PROJECT_NAME_EXIST.msg)

        # 保存或更新项目信息
        result = await ProjectInfo.create_or_update(params.dict())
        return result

    @staticmethod
    async def deleted(params: ProjectDel) -> int:
        """
        删除项目
        :param params:
        :return:
        """
        pass


