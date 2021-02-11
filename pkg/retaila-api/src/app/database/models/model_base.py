from bson.objectid import ObjectId as BsonObjectId
from fastapi import status

from fastapi.responses import JSONResponse


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


def ResponseModel(code=status.HTTP_200_OK, message="Generic response. WIP to be implemented.", data=""):
    body = {
        "code": code,
        "message": message,
        "data": [data],
    }

    return JSONResponse(
        status_code=code,
        content=body
    )


def ErrorResponseModel(code=status.HTTP_400_BAD_REQUEST, error_message="Generic error occurred."):
    body = {
        "code": code,
        "message": "An error occurred.",
        "error_message": error_message,
    }

    return JSONResponse(
        status_code=code,
        content=body
    )
