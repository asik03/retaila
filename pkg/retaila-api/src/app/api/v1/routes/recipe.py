from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from app.core.logic.recipe import retrieve_recipes, add_recipe, retrieve_recipe, update_recipe, delete_recipe
from app.core.models.model_base import ResponseModel, ErrorResponseModel
from app.core.models.recipe import RecipeSchema, UpdateRecipeModel

recipe_router = APIRouter()


@recipe_router.get("/", response_description="Recipes retrieved")
async def get_recipes():
    recipes = await retrieve_recipes()
    if recipes:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=recipes,
            message="Recipes data retrieved successfully"
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        data=recipes,
        message="Empty list returned"
    )


@recipe_router.post("/", response_description="Recipe data added into the database")
async def add_recipe_data(recipe: RecipeSchema = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(recipe)
    if new_recipe.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=new_recipe.data,
            message="Recipe added successfully."
        )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_recipe.error_message,
        )


@recipe_router.get("/{id}", response_description="Recipe data retrieved")
async def get_recipe_data(id: str):
    recipe = await retrieve_recipe(id)
    if recipe:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=recipe,
            message="Recipe data retrieved successfully"
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Recipe '{}' doesn't exist.".format(id)

    )


@recipe_router.put("/{id}")
async def update_recipe_data(id: str, req: UpdateRecipeModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_recipe = await update_recipe(id, req)
    if updated_recipe.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Recipe with ID: {} name update is successful".format(id),
            data=updated_recipe.data,
        )
    else:
        return ErrorResponseModel(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_message=updated_recipe.error_message,
        )


@recipe_router.delete("/{id}", response_description="Recipe data deleted from the database")
async def delete_recipe_data(id: str):
    deleted_recipe = await delete_recipe(id)
    if deleted_recipe.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Recipe with ID: {} removed".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message=deleted_recipe.error_message
    )
