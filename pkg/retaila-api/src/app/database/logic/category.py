from pymongo.errors import DuplicateKeyError
from app.database.database import database, ResultGeneric
from app.database.utils import check_empty_body_request, check_pk_in_collection, delete_item_from_collection, \
    get_item_from_collection

category_collection = database.get_collection("categories_collection")


def category_helper(category) -> dict:
    return {
        "id": str(category["_id"]),
    }


# Retrieve all categories present in the database
async def retrieve_categories():
    categories = []
    async for category in category_collection.find():
        categories.append(category_helper(category))
    return categories


# Retrieve a category with a matching ID
async def retrieve_category(_id: str) -> dict:
    category = await get_item_from_collection(_id=_id, collection=category_collection)
    if category.status:
        return category_helper(category.data)


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
async def update_category(_id: str, category_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(category_data)
    if not result.status:
        return result

    # Check if the category exists
    result = check_pk_in_collection(object_type="category", object_id=_id, result=result)
    if not result.status:
        return result

    # Update the category
    updated_category = await category_collection.update_one(
        {"_id": _id}, {"$set": category_data}
    )
    if updated_category:
        result.status = True
        category_updated = await category_collection.find_one({"_id": _id})
        result.data = category_helper(category_updated)
    else:
        result.status = False
        result.error_message.append("There was a problem while updating the category with id {} into the database".format(_id))
    return result


# Delete a category from the database
async def delete_category(_id: str):
    return await delete_item_from_collection(_id=_id, collection=category_collection)



