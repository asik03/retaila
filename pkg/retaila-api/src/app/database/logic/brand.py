from typing import Type

from pymongo.errors import DuplicateKeyError

from src.app.database.database import database, ResultGeneric, check_empty_body_request

brand_collection = database.get_collection("brands_collection")


def brand_helper(brand) -> dict:
    print(str(brand))
    return {
        "id": str(brand["_id"]),
        "super_private_brand": brand["super_private_brand"],
    }


# Retrieve all brands present in the database
async def retrieve_brands():
    brands = []
    async for brand in brand_collection.find():
        brands.append(brand_helper(brand))
    return brands


# Retrieve a brand with a matching ID
async def retrieve_brand(id: str) -> dict:
    brand = await brand_collection.find_one({"_id": id})
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
    result = check_empty_body_request(brand_data)
    if not result.status:
        return result

    # Check if the brand exists
    brand = await brand_collection.find_one({"_id": id})
    if not brand:
        result.error_message.append("Brand id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # Update the brand
    updated_brand = await brand_collection.update_one(
        {"_id": id}, {"$set": brand_data}
    )
    if updated_brand:
        result.status = True
        brand_updated = await brand_collection.find_one({"_id": id})
        result.data = brand_helper(brand_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the brand with id {} into the database".format(id))
    return result


# Delete a brand from the database
async def delete_brand(id: str):
    brand = await brand_collection.find_one({"_id": id})
    if brand:
        await brand_collection.delete_one({"_id": id})
        return True
