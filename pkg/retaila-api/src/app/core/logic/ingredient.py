from pymongo.errors import DuplicateKeyError
from app.core.database import database, ResultGeneric
from app.core.utils import check_empty_body_request, check_pk_in_collection, delete_item_from_collection, \
    get_item_from_collection, is_object_id_map_dict

ingredient_collection = database.get_collection("ingredient_collection")


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
    ingredient = await get_item_from_collection(_id=_id, collection=ingredient_collection)
    if ingredient.status:
        return ingredient_helper(ingredient.data)


# Add a new ingredient into to the database
async def add_ingredient(ingredient_data: dict) -> ResultGeneric:
    result = ResultGeneric().reset()
    result.status = True

    try:
        ingredient = await ingredient_collection.insert_one(ingredient_data)
        new_ingredient = await ingredient_collection.find_one({"_id": ingredient.inserted_id})
        result.data = ingredient_helper(new_ingredient)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Ingredient '{}' already exists in the database!".format(ingredient_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a ingredient with a matching ID
async def update_ingredient(_id: str, ingredient_data: dict):
    result = ResultGeneric().reset()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(ingredient_data, result)
    if not result.status:
        return result

    # Check if the ingredient exists
    result = await check_pk_in_collection(object_type="ingredient", _id=_id, result=result)
    if not result.status:
        return result

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
        result.error_message.append(
            "There was a problem while updating the ingredient with id {} into the database".format(_id)
        )
    return result


# Delete a ingredient from the database
async def delete_ingredient(_id: str):
    return await delete_item_from_collection(_id=_id, collection=ingredient_collection)

