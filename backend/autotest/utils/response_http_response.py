"""
# -*- coding:utf-8 -*-
# @Author: Beck
# @File: response_http_response.py
# @Date: 2023/12/12 17:19
"""

import typing

from loguru import logger
from starlette import status
from starlette.responses import JSONResponse, Response

from autotest.utils.local import g
from autotest.utils.response_code import CodeEnum
from autotest.utils.serialize import default_serialize

import orjson


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_PASSTHROUGH_DATETIME,
            default=default_serialize
        )


def partner_success(
    data=None,
    code=CodeEnum.PARTNER_CODE_OK.code,
    msg=CodeEnum.PARTNER_CODE_OK.msg,
    http_code=status.HTTP_200_OK,
    headers=None):
    """
    通用结果返回
    :param data: 返回数据
    :param code: 状态码
    :param http_code: http状态码
    :param msg: 返回消息
    :param headers: 响应头
    :return:
    """
    if data is None:
        data = {}

    success = True if code == CodeEnum.PARTNER_CODE_OK.code else False
    content = dict(code=code, msg=msg, data=data, success=success, trace_id=g.trace_id)
    content = default_serialize(content)
    return ORJSONResponse(status_code=http_code, content=content, headers=headers)


def create_response(status_code: int, code: int, msg: str, data: typing.Any = None, headers: dict = None) -> Response:
    """创建一个 ORJSONResponse 对象。"""
    return ORJSONResponse(status_code=status_code, content={'code': code, 'msg': msg, 'data': data}, headers=headers)


def resp_200(*, data: typing.Any = '', msg: str = "Success") -> dict:
    logger.info(msg)
    return {'code': 200, 'data': data, 'msg': msg}


def resp_400(code: int = 400, data: str = None, msg: str = "请求错误(400)") -> Response:
    return create_response(status.HTTP_400_BAD_REQUEST, code, msg, data)


def resp_401(*, data: str = None, msg: str = "未授权，请重新登录(401)") -> Response:
    return create_response(status.HTTP_401_UNAUTHORIZED, 401, msg, data)


def resp_403(*, data: str = None, msg: str = "拒绝访问(403)") -> Response:
    return create_response(status.HTTP_403_FORBIDDEN, 403, msg, data)


def resp_404(*, data: str = None, msg: str = "请求出错(404)") -> Response:
    return create_response(status.HTTP_404_NOT_FOUND, 404, msg, data)


def resp_422(*, data: str = None, msg: typing.Union[list, dict, str] = "不可处理的实体") -> Response:
    return create_response(status.HTTP_422_UNPROCESSABLE_ENTITY,
                           422, msg, data)


def resp_500(*, data: str = None, msg: typing.Union[list, dict, str] = "服务器错误(500)") -> Response:
    return ORJSONResponse(headers={'Access-Control-Allow-Origin': '*'},
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          content={'code': 500, 'msg': msg, 'data': data})


def resp_502(*, data: str = None, msg: str = "网络错误(502)") -> Response:
    return create_response(status.HTTP_502_BAD_GATEWAY, 502, msg, data)


# ------------------------------------------- 以下不常用 -------------------------------------------

def resp_406(*, data: str = None, msg: str = "请求的格式不可得(406)") -> Response:
    return create_response(status.HTTP_406_NOT_ACCEPTABLE, 406, msg, data)


def resp_408(*, data: str = None, msg: str = "请求超时(408)") -> Response:
    return create_response(status.HTTP_408_REQUEST_TIMEOUT, 408, msg, data)


def resp_410(*, data: str = None, msg: str = "请求的资源被永久删除，且不会再得到的(410)") -> Response:
    return create_response(status.HTTP_410_GONE, 410, msg, data)


def resp_501(*, data: str = None, msg: str = "服务未实现(501)") -> Response:
    return create_response(status.HTTP_501_NOT_IMPLEMENTED, 501, msg, data)


def resp_503(*, data: str = None, msg: str = "服务不可用(503)") -> Response:
    return create_response(status.HTTP_503_SERVICE_UNAVAILABLE,
                           503, msg, data)


def resp_504(*, data: str = None, msg: str = "网络超时(504)") -> Response:
    return create_response(status.HTTP_504_GATEWAY_TIMEOUT, 504, msg, data)


def resp_505(*, data: str = None, msg: str = "HTTP版本不受支持(505)") -> Response:
    return create_response(status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
                           505, msg, data)
