from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from src.app.database.logic.ingredient import (
    add_ingredient,
    delete_ingredient,
    retrieve_ingredient,
    retrieve_ingredients,
    update_ingredient,
)
from src.app.database.models.model_base import ResponseModel, ErrorResponseModel
from src.app.database.models.ingredient import (
    IngredientSchema,
    UpdateIngredientModel,
)


ingredient_router = APIRouter()


@ingredient_router.get("/", response_description="Ingredients retrieved")
async def get_ingredients():
    ingredients = await retrieve_ingredients()
    if ingredients:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Ingredients data retrieved successfully",
            data=ingredients
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        message="Empty list returned",
        data=ingredients
    )


@ingredient_router.post("/",)
async def add_ingredient_data(ingredient: IngredientSchema = Body(...)):
    ingredient = jsonable_encoder(ingredient)
    new_ingredient = await add_ingredient(ingredient)
    if new_ingredient.status:
        return ResponseModel(
            code=status.HTTP_201_CREATED,
            message="Ingredient added successfully.",
            data=new_ingredient.data,
            )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_ingredient.error_message,
        )


@ingredient_router.get("/{id}", response_description="Ingredient data retrieved")
async def get_ingredient_data(id: str):
    ingredient = await retrieve_ingredient(id)
    if ingredient:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=ingredient,
            message="Ingredient data retrieved successfully"
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Ingredient doesn't exist.",
    )


@ingredient_router.put("/{id}")
async def update_ingredient_data(id: str, req: UpdateIngredientModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_ingredient = await update_ingredient(id, req)

    if updated_ingredient.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Ingredient with ID: {} name update is successful".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=updated_ingredient.error_message,
    )


@ingredient_router.delete("/{id}", response_description="Ingredient data deleted from the database")
async def delete_ingredient_data(id: str):
    deleted_ingredient = await delete_ingredient(id)
    if deleted_ingredient:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Ingredient with ID: {} removed".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message="Ingredient with id {0} doesn't exist".format(id)
    )
