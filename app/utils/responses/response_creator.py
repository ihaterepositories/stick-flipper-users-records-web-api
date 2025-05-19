from app.utils.responses.models.base_response import BaseResponse
from fastapi.responses import JSONResponse
from typing import Any

def ok(data: Any = None) -> JSONResponse:
    response = BaseResponse(
        status_code=200,
        error_description=None,
        data=data
    )
    return JSONResponse(status_code=200, content=response.model_dump())

def bad_request(description: str = None) -> JSONResponse:
    response = BaseResponse(
        status_code=400,
        error_description=description,
        data=None
    )
    return JSONResponse(status_code=400, content=response.model_dump())

def server_error(description: str = None) -> JSONResponse:
    response = BaseResponse(
        status_code=500,
        error_description=description,
        data=None
    )
    return JSONResponse(status_code=500, content=response.model_dump())