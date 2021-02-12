from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.database.database import database, ResultGeneric, check_empty_body_request
from src.app.database.logic.ingredient import ingredient_collection

recipe_collection = database.get_collection("recipes_collection")


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "recipe_name": recipe["recipe_name"],
        "author_key": recipe["author_key"],
        "ingredients": recipe["ingredients"],
        "steps": recipe["steps"],
        "extra_notes": recipe["extra_notes"],
    }


# Retrieve all recipes present in the database
async def retrieve_recipes():
    recipes = []
    async for recipe in recipe_collection.find():
        recipes.append(recipe_helper(recipe))
    return recipes


# Retrieve a recipe with a matching ID
async def retrieve_recipe(id: str) -> dict:
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        return recipe_helper(recipe)


# Add a new recipe into to the database
async def add_recipe(recipe_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    result.status = True

    # Check if the ingredients of the recipe exists in the database
    for ingredient in recipe_data.get("ingredients"):
        ingredient_key = ingredient.get("ingredient_key")
        if not await ingredient_collection.find_one({"_id": ingredient_key}):
            result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
            result.status = False
    if not result.status:
        # Return to avoid the updating
        return result

    # Adding the recipe into the database
    try:
        recipe = await recipe_collection.insert_one(recipe_data)
        new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
        result.data = recipe_helper(new_recipe)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Recipe '{}' already exists in the database!".format(recipe_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a recipe with a matching ID
async def update_recipe(id: str, recipe_data: dict):
    result = ResultGeneric
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(recipe_data)
    if not result.status:
        return result

    # Check if the recipe exists
    if not await recipe_collection.find_one({"_id": ObjectId(id)}):
        result.error_message.append("Recipe id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # # Check if the author exists
    # author_key = recipe_data.get("author_id")
    # if not await author_collection.find_one({"_id": author_key}):
    #     result.error_message.append("Author id {} doesn't exist in the database.".format(id))
    #     result.status = False
    #     return result

    # Check if the ingredients of the recipe exists in the database
    for ingredient in recipe_data.get("ingredients"):
        ingredient_key = ingredient.get("ingredient_key")
        if not await ingredient_collection.find_one({"_id": ingredient_key}):
            result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
            result.status = False
    if not result.status:
        # Return to avoid the updating
        return result

    # Update the recipe
    updated_recipe = await recipe_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": recipe_data}
    )
    if updated_recipe:
        result.status = True
        recipe_updated = await recipe_collection.find_one({"_id": ObjectId(id)})
        result.data = recipe_helper(recipe_updated)
    else:
        result.status = False
        result.error_message.append("There was a problem while updating the recipe with id {} into the database".format(id))
    return result


# Delete a recipe from the database
async def delete_recipe(id: str):
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        await recipe_collection.delete_one({"_id": ObjectId(id)})
        return True


