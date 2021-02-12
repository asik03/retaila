from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from src.app.database.logic.category import (
    add_category,
    delete_category,
    retrieve_category,
    update_category,
    retrieve_categories,
)
from src.app.database.models.model_base import ResponseModel, ErrorResponseModel
from src.app.database.models.category import (
    CategorySchema,
    UpdateCategoryModel,
)


category_router = APIRouter()


@category_router.get("/", response_description="Categories retrieved")
async def get_categories():
    categories = await retrieve_categories()
    if categories:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Categories data retrieved successfully",
            data=categories
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        message="Empty list returned",
        data=categories
    )


@category_router.post("/",)
async def add_category_data(category: CategorySchema = Body(...)):
    category = jsonable_encoder(category)
    new_category = await add_category(category)
    if new_category.status:
        return ResponseModel(
            code=status.HTTP_201_CREATED,
            message="Category added successfully.",
            data=new_category.data,
            )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_category.error_message,
        )


@category_router.get("/{id}", response_description="Category data retrieved")
async def get_category_data(id: str):
    category = await retrieve_category(id)
    if category:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=category,
            message="Category data retrieved successfully"
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Category doesn't exist.",
    )


@category_router.put("/{id}")
async def update_category_data(id: str, req: UpdateCategoryModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_category = await update_category(id, req)

    if updated_category.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Category with ID: {} name update is successful".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=updated_category.error_message,
    )


@category_router.delete("/{id}", response_description="Category data deleted from the database")
async def delete_category_data(id: str):
    deleted_category = await delete_category(id)
    if deleted_category:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Category with ID: {} removed".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message="Category with id {0} doesn't exist".format(id)
    )
