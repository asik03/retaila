from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from app.core.logic.brand import add_brand, retrieve_brands, retrieve_brand, update_brand, \
    delete_brand
from app.core.models.brand import BrandSchema, UpdateBrandModel
from app.core.models.model_base import ResponseModel, ErrorResponseModel

brand_router = APIRouter()


@brand_router.get("/", response_description="Brands retrieved")
async def get_brands():
    brands = await retrieve_brands()
    if brands:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Brands data retrieved successfully",
            data=brands,
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        message="Empty list returned",
        data=""
    )


@brand_router.post("/")
async def add_brand_data(brand: BrandSchema = Body(...)):
    brand = jsonable_encoder(brand)
    new_brand = await add_brand(brand)
    if new_brand.status:
        return ResponseModel(
            code=status.HTTP_201_CREATED,
            message="Brand added successfully.",
            data=new_brand.data,
        )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_brand.error_message,
        )


@brand_router.get("/{id}", response_description="Brand data retrieved")
async def get_brand_data(id: str):
    brand = await retrieve_brand(id)
    if brand:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=brand,
            message="Brand data retrieved successfully")
    return ErrorResponseModel(
            code=status.HTTP_404_NOT_FOUND,
            error_message="Brand '{}' doesn't exist.".format(id)
    )


@brand_router.put("/{id}")
async def update_brand_data(id: str, req: UpdateBrandModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_brand = await update_brand(id, req)

    if updated_brand.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Brand with ID: {} name update is successful".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=updated_brand.error_message,
    )


@brand_router.delete("/{id}", response_description="Brand data deleted from the database")
async def delete_brand_data(id: str):
    deleted_brand = await delete_brand(id)
    if deleted_brand.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Brand with ID: {} removed".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=deleted_brand.error_message
    )
