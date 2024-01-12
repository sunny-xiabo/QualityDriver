"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: project.py
# @Date: 2024/1/12 22:38
"""
from fastapi import APIRouter

from autotest.schemas.api.project import ProjectQuery, ProjectInfo
from autotest.services.api.project import ProjectService
from autotest.utils.response_http_response import partner_success

router = APIRouter()


@router.post("/list", description="项目列表")
async def project_list(params: ProjectQuery):
    data = await ProjectService.list(params)
    return partner_success(data)


@router.post("/getAllProject", description="获取所有项目")
async def get_all_project():
    data = await ProjectService.get_all()
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存或更新项目")
async def save_or_update_project(params: ProjectInfo):
    data = await ProjectService.save_or_update(params)
    return partner_success(data)
