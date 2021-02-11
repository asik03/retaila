from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.app.database.logic.recipe import (
    add_recipe,
    delete_recipe,
    retrieve_recipe,
    retrieve_recipes,
    update_recipe,
)
from src.app.database.models.model_base import ResponseModel, ErrorResponseModel
from src.app.database.models.recipe import (
    RecipeSchema,
    UpdateRecipeModel,
)

recipe_router = APIRouter()


@recipe_router.get("/", response_description="Recipes retrieved")
async def get_recipes():
    recipes = await retrieve_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@recipe_router.post("/", response_description="Recipe data added into the database")
async def add_recipe_data(recipe: RecipeSchema = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(recipe)
    if new_recipe.status:
        return ResponseModel(new_recipe.data, "Recipe added successfully.")
    else:
        return ErrorResponseModel(
            "An error ocurred",
            404,
            new_recipe.error_message,
        )


@recipe_router.get("/{id}", response_description="Recipe data retrieved")
async def get_recipe_data(id: str):
    recipe = await retrieve_recipe(id)
    if recipe:
        return ResponseModel(recipe, "Recipe data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recipe doesn't exist.")


@recipe_router.put("/{id}")
async def update_recipe_data(id: str, req: UpdateRecipeModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_recipe = await update_recipe(id, req)
    if updated_recipe.status:
        return ResponseModel(
            updated_recipe.data,
            "Recipe with ID: {} name update is successful".format(id),
        )
    else:
        return ErrorResponseModel(
            "An error occurred",
            404,
            updated_recipe.error_message,
        )


@recipe_router.delete("/{id}", response_description="Recipe data deleted from the database")
async def delete_recipe_data(id: str):
    deleted_recipe = await delete_recipe(id)
    if deleted_recipe:
        return ResponseModel(
            "Recipe with ID: {} removed".format(id), "Recipe deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "Recipe with id {0} doesn't exist".format(id)
    )
