from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.database.database import database, category_helper, ResultGeneric, checkEmptyBodyRequest

category_collection = database.get_collection("categories_collection")


# Retrieve all categories present in the database
async def retrieve_categories():
    categories = []
    async for category in category_collection.find():
        categories.append(category_helper(category))
    return categories


# Retrieve a category with a matching ID
async def retrieve_category(id: str) -> dict:
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        return category_helper(category)


# Add a new category into to the database
async def add_category(category_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    result.status = True

    try:
        category = await category_collection.insert_one(category_data)
        new_category = await category_collection.find_one({"_id": category.inserted_id})
        result.data = category_helper(new_category)
        result.status = True
    except DuplicateKeyError:
        result.error_message = "Category '{}' already exists in the database!".format(category_data.get("_id"))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a category with a matching ID
async def update_category(id: str, category_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = checkEmptyBodyRequest(category_data)
    if not result.status:
        return result

    # Check if the category exists
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if not category:
        result.error_message.append("Category id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # Update the category
    updated_category = await category_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": category_data}
    )
    if updated_category:
        result.status = True
        category_updated = await category_collection.find_one({"_id": ObjectId(id)})
        result.data = category_helper(category_updated)
    else:
        result.status = False
        result.error_message.append("There was a problem while updating the category with id {} into the database".format(id))
    return result


# Delete a category from the database
async def delete_category(id: str):
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        await category_collection.delete_one({"_id": ObjectId(id)})
        return True
