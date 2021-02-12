from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from src.app.database.logic.product import (

    retrieve_product, add_product, delete_product, update_product, retrieve_products)
from src.app.database.models.model_base import ResponseModel, ErrorResponseModel
from src.app.database.models.product import (
    ProductSchema, UpdateProductModel
)

product_router = APIRouter()


@product_router.get("/", response_description="Products retrieved")
async def get_products():
    products = await retrieve_products()
    if products:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=products,
            message="Products data retrieved successfully"
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        data=products,
        message="Empty list returned"
    )


@product_router.post("/", response_description="Product data added into the database")
async def add_product_data(product: ProductSchema = Body(...)):
    product = jsonable_encoder(product)
    new_product = await add_product(product)
    if new_product.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=new_product.data,
            message="Product added successfully."
        )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_product.error_message,
        )


@product_router.get("/{id}", response_description="Product data retrieved")
async def get_product_data(id: str):
    product = await retrieve_product(id)
    if product:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=product,
            message="Product data retrieved successfully"
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Product doesn't exist."
    )


@product_router.put("/{id}")
async def update_product_data(id: str, req: UpdateProductModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_product = await update_product(id, req)
    if updated_product.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Product with ID: {} name update is successful".format(id),
            data=updated_product.data,
        )
    else:
        return ErrorResponseModel(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_message=updated_product.error_message,
        )


@product_router.delete("/{id}", response_description="Product data deleted from the database")
async def delete_product_data(id: str):
    deleted_product = await delete_product(id)
    if deleted_product:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Product with ID: {} removed".format(id),
            data=""
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Product with id {0} doesn't exist".format(id)
    )
