from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.database.database import database, ResultGeneric, checkEmptyBodyRequest
from src.app.database.models.brand import brand_helper

brand_collection = database.get_collection("brands_collection")


# Retrieve all brands present in the database
async def retrieve_brands():
    brands = []
    async for brand in brand_collection.find():
        brands.append(brand_helper(brand))
    return brands


# Retrieve a brand with a matching ID
async def retrieve_brand(id: str) -> dict:
    brand = await brand_collection.find_one({"_id": ObjectId(id)})
    if brand:
        return brand_helper(brand)


# Add a new brand into to the database
async def add_brand(brand_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    result.status = True

    try:
        brand = await brand_collection.insert_one(brand_data)
        new_brand = await brand_collection.find_one({"_id": brand.inserted_id})
        result.data = brand_helper(new_brand)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Brand '{}' already exists in the database!".format(brand_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a brand with a matching ID
async def update_brand(id: str, brand_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = checkEmptyBodyRequest(brand_data)
    if not result.status:
        return result

    # Check if the brand exists # TODO: change this with new _id format
    brand = await brand_collection.find_one({"_id": ObjectId(id)})
    if not brand:
        result.error_message.append("Brand id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # Check if the brand_id has the same name of the the brand_id to be updated
    if not brand.get("brand_id") == brand_data.get("brand_id"):
        result.error_message.append(
            "brand_id {} is not the same as the one with the id {} in the database.".format(brand.get("brand_id"), id))
        result.status = False
        return result

    # Update the brand
    updated_brand = await brand_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": brand_data}
    )
    if updated_brand:
        result.status = True
        brand_updated = await brand_collection.find_one({"_id": ObjectId(id)})
        result.data = brand_helper(brand_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the brand with id {} into the database".format(id))
    return result


# Delete a brand from the database
async def delete_brand(id: str):
    brand = await brand_collection.find_one({"_id": ObjectId(id)})
    if brand:
        await brand_collection.delete_one({"_id": ObjectId(id)})
        return True
