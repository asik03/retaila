from fastapi import APIRouter, Body
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
        return ResponseModel(ingredients, "Ingredients data retrieved successfully")
    return ResponseModel(ingredients, "Empty list returned")


@ingredient_router.post("/",)
async def add_ingredient_data(ingredient: IngredientSchema = Body(...)):
    ingredient = jsonable_encoder(ingredient)
    new_ingredient = await add_ingredient(ingredient)
    if new_ingredient.status:
        return ResponseModel(
            new_ingredient.data,
            "Ingredient added successfully.")
    else:
        return ErrorResponseModel(
            "An error occurred",
            404,
            new_ingredient.error_message,
        )


@ingredient_router.get("/{id}", response_description="Ingredient data retrieved")
async def get_ingredient_data(id: str):
    ingredient = await retrieve_ingredient(id)
    if ingredient:
        return ResponseModel(ingredient, "Ingredient data retrieved successfully")
    return ErrorResponseModel(
        "An error occurred.",
        404,
        "Ingredient doesn't exist.")


@ingredient_router.put("/{id}")
async def update_ingredient_data(id: str, req: UpdateIngredientModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_ingredient = await update_ingredient(id, req)

    if updated_ingredient.status:
        return ResponseModel(
            "Ingredient with ID: {} name update is successful".format(id),
            "Ingredient name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        updated_ingredient.error_message,
    )


@ingredient_router.delete("/{id}", response_description="Ingredient data deleted from the database")
async def delete_ingredient_data(id: str):
    deleted_ingredient = await delete_ingredient(id)
    if deleted_ingredient:
        return ResponseModel(
            "Ingredient with ID: {} removed".format(id), "Ingredient deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "Ingredient with id {0} doesn't exist".format(id)
    )
