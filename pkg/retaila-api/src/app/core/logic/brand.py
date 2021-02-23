from pymongo.errors import DuplicateKeyError

from app.core.database import database, ResultGeneric
from app.core.utils import check_empty_body_request, check_pk_in_collection, delete_item_from_collection, \
    get_item_from_collection

brand_collection = database.get_collection("brand_collection")


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
async def retrieve_brand(_id: str) -> dict:
    brand = await get_item_from_collection(_id=_id, collection=brand_collection)
    if brand.status:
        return brand_helper(brand.data)


# Add a new brand into to the database
async def add_brand(brand_data: dict) -> ResultGeneric:
    result = ResultGeneric().reset()
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
async def update_brand(_id: str, brand_data: dict):
    result = ResultGeneric().reset()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(data=brand_data, result=result)
    if not result.status:
        return result

    # Check if the brand exists
    result = await check_pk_in_collection(object_type="brand", _id=_id, result=result)

    if not result.status:
        return result

    # Update the brand
    updated_brand = await brand_collection.update_one(
        {"_id": _id}, {"$set": brand_data}
    )
    if updated_brand:
        result.status = True
        brand_updated = await brand_collection.find_one({"_id": _id})
        result.data = brand_helper(brand_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the brand with id {} into the database".format(_id))
    return result


# Delete a brand from the database
async def delete_brand(_id: str):
    return await delete_item_from_collection(_id=_id, collection=brand_collection)

