from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from src.app.database import (
    add_recipe,
    delete_recipe,
    retrieve_recipe,
    retrieve_recipes,
    update_recipe,
)
from src.app.models.recipe import (
    ErrorResponseModel,
    ResponseModel,
    RecipeSchema,
    UpdateRecipeModel,
)

router = APIRouter()


@router.post("/", response_description="Recipe data added into the database")
async def add_recipe_data(recipe: RecipeSchema = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(recipe)
    return ResponseModel(new_recipe, "Recipes added successfully.")


@router.get("/", response_description="Recipes retrieved")
async def get_recipes():
    recipes = await retrieve_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/{id}", response_description="Recipe data retrieved")
async def get_recipe_data(id: str):
    recipe = await retrieve_recipe(id)
    if recipe:
        return ResponseModel(recipe, "Recipe data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recipe doesn't exist.")


@router.put("/{id}")
async def update_recipe_data(id: str, req: UpdateRecipeModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_recipe = await update_recipe(id, req)
    if updated_recipe:
        return ResponseModel(
            "Recipe with ID: {} name update is successful".format(id),
            "Recipe name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the recipe data.",
    )


@router.delete("/{id}", response_description="Recipe data deleted from the database")
async def delete_recipe_data(id: str):
    deleted_recipe = await delete_recipe(id)
    if deleted_recipe:
        return ResponseModel(
            "Recipe with ID: {} removed".format(id), "Recipe deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Recipe with id {0} doesn't exist".format(id)
    )
