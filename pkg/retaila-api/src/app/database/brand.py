from bson import ObjectId

from src.app.database.database import database, brand_helper, ResultGeneric, checkEmptyBodyRequest

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

    # Check if the brand already exist in the database
    brand_key = brand_data.get("brand_key")
    if await brand_collection.find_one({"brand_key": brand_key}):
        result.error_message = "Brand_key {} already exists in the database!".format(brand_key)
        result.status = False
    else:
        brand = await brand_collection.insert_one(brand_data)
        new_brand = await brand_collection.find_one({"_id": brand.inserted_id})
        result.data = brand_helper(new_brand)
        result.status = True

    return result


# Update a brand with a matching ID
async def update_brand(id: str, brand_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = checkEmptyBodyRequest(brand_data)
    if not result.status:
        return result

    # Check if the recipe exists
    brand = await brand_collection.find_one({"_id": ObjectId(id)})
    if not brand:
        result.error_message.append("Brand id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # Check if the brand_key has the same name of the the brand_key to be updated
    if not brand.get("brand_key") == brand_data.get("brand_key"):
        result.error_message.append("Brand_key {} is not the same as the one with the id {} in the database.".format(brand.get("brand_key"), id))
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
