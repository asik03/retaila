from typing import Type
from pymongo.errors import DuplicateKeyError
from src.app.database.database import database, ResultGeneric
from src.app.database.utils import check_empty_body_request, check_pk_in_collection

ingredient_collection = database.get_collection("ingredients_collection")


def ingredient_helper(ingredient) -> dict:
    return {
        "id": str(ingredient["_id"]),
    }


# Retrieve all ingredients present in the database
async def retrieve_ingredients():
    ingredients = []
    async for ingredient in ingredient_collection.find():
        ingredients.append(ingredient_helper(ingredient))
    return ingredients


# Retrieve a ingredient with a matching ID
async def retrieve_ingredient(_id: str) -> dict:
    ingredient = await ingredient_collection.find_one({"_id": _id})
    if ingredient:
        return ingredient_helper(ingredient)


# Add a new ingredient into to the database
async def add_ingredient(ingredient_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    result.status = True

    try:
        ingredient = await ingredient_collection.insert_one(ingredient_data)
        new_ingredient = await ingredient_collection.find_one({"_id": ingredient.inserted_id})
        result.data = ingredient_helper(new_ingredient)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("ingredient '{}' already exists in the database!".format(ingredient_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a ingredient with a matching ID
async def update_ingredient(_id: str, ingredient_data: dict):
    result = ResultGeneric
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(ingredient_data)
    if not result.status:
        return result

    # Check if the ingredient exists
    result = check_pk_in_collection(object_type="ingredient", object_id=_id, result=result)
    # ingredient = await ingredient_collection.find_one({"_id": _id})
    # if not ingredient:
    #     result.error_message.append("Ingredient id {} doesn't exist in the database.".format(_id))
    #     result.status = False
    #     return result

    # Update the ingredient
    updated_ingredient = await ingredient_collection.update_one(
        {"_id": _id}, {"$set": ingredient_data}
    )
    if updated_ingredient:
        result.status = True
        ingredient_updated = await ingredient_collection.find_one({"_id": _id})
        result.data = ingredient_helper(ingredient_updated)
    else:
        result.status = False
        result.error_message.append("There was a problem while updating the ingredient with id {} into the database".format(_id))
    return result


async def delete_ingredient(_id: str):
    # Delete a ingredient from the database
    result = ResultGeneric()
    result.status = True

    # Delete ingredient
    if await ingredient_collection.find_one({"_id": _id}):
        await ingredient_collection.delete_one({"_id": _id})
        result.status = True
        return result
    else:
        result.status = False
        result.error_message.append("Couldn't find the ingredient ID to delete")




