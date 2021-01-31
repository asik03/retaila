from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.app.database.brand import (
    add_brand,
    delete_brand,
    retrieve_brand,
    retrieve_brands,
    update_brand,
)
from src.app.models.model_base import ResponseModel, ErrorResponseModel
from src.app.models.brand import (
    BrandSchema,
    UpdateBrandModel,
)


brand_router = APIRouter()


@brand_router.get("/", response_description="Brands retrieved")
async def get_brands():
    brands = await retrieve_brands()
    if brands:
        return ResponseModel(brands, "Brands data retrieved successfully")
    return ResponseModel(brands, "Empty list returned")


@brand_router.post("/",)
async def add_brand_data(brand: BrandSchema = Body(...)):
    brand = jsonable_encoder(brand)
    new_brand = await add_brand(brand)
    if new_brand.status:
        return ResponseModel(
            new_brand.data,
            "Brand added successfully.")
    else:
        raise ErrorResponseModel(
            "An error occurred",
            404,
            new_brand.error_message,
        )


@brand_router.get("/{id}", response_description="Brand data retrieved")
async def get_brand_data(id: str):
    brand = await retrieve_brand(id)
    if brand:
        return ResponseModel(brand, "Brand data retrieved successfully")
    raise ErrorResponseModel(
        "An error occurred.",
        404,
        "Brand doesn't exist.")


@brand_router.put("/{id}")
async def update_brand_data(id: str, req: UpdateBrandModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_brand = await update_brand(id, req)

    if updated_brand.status:
        return ResponseModel(
            "Brand with ID: {} name update is successful".format(id),
            "Brand name updated successfully",
        )
    raise ErrorResponseModel(
        "An error occurred",
        404,
        updated_brand.error_message,
    )


@brand_router.delete("/{id}", response_description="Brand data deleted from the database")
async def delete_brand_data(id: str):
    deleted_brand = await delete_brand(id)
    if deleted_brand:
        return ResponseModel(
            "Brand with ID: {} removed".format(id), "Brand deleted successfully"
        )
    raise ErrorResponseModel(
        "An error occurred",
        404,
        "Brand with id {0} doesn't exist".format(id)
    )
