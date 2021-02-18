from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from app.core.logic.supermarket_local import retrieve_supermarket_locals, add_supermarket_local, \
    retrieve_supermarket_local, update_supermarket_local, delete_supermarket_local
from app.core.models.model_base import ResponseModel, ErrorResponseModel
from app.core.models.supermarket_local import SupermarketLocalSchema, UpdateSupermarketLocalModel

supermarket_local_router = APIRouter()


@supermarket_local_router.get("/", response_description="Supermarket_locals retrieved")
async def get_supermarket_locals():
    supermarket_locals = await retrieve_supermarket_locals()
    if supermarket_locals:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Supermarket_locals data retrieved successfully",
            data=supermarket_locals
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        message="Empty list returned",
        data=supermarket_locals
    )


@supermarket_local_router.post("/",)
async def add_supermarket_local_data(supermarket_local: SupermarketLocalSchema = Body(...)):
    supermarket_local = jsonable_encoder(supermarket_local)
    new_supermarket_local = await add_supermarket_local(supermarket_local)
    if new_supermarket_local.status:
        return ResponseModel(
            code=status.HTTP_201_CREATED,
            message="Supermarket_local added successfully.",
            data=new_supermarket_local.data,
            )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_supermarket_local.error_message,
        )


@supermarket_local_router.get("/{id}", response_description="Supermarket_local data retrieved")
async def get_supermarket_local_data(id: str):
    supermarket_local = await retrieve_supermarket_local(id)
    if supermarket_local:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=supermarket_local,
            message="Supermarket_locals data retrieved successfully"
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Supermarket_local doesn't exist.",
    )


@supermarket_local_router.put("/{id}")
async def update_supermarket_local_data(id: str, req: UpdateSupermarketLocalModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_supermarket_local = await update_supermarket_local(id, req)

    if updated_supermarket_local.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Supermarket_local with ID: {} name update is successful".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=updated_supermarket_local.error_message,
    )


@supermarket_local_router.delete("/{id}", response_description="Supermarket_local data deleted from the database")
async def delete_supermarket_local_data(id: str):
    deleted_supermarket_local = await delete_supermarket_local(id)
    if deleted_supermarket_local.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Supermarket_local with ID: {} removed".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=deleted_supermarket_local.error_message
    )
