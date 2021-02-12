from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.database.logic.brand import brand_collection
from src.app.database.logic.category import category_collection
from src.app.database.database import ResultGeneric, database
from src.app.database.utils import check_empty_body_request, check_pk_in_collection
from src.app.database.logic.ingredient import ingredient_collection

product_collection = database.get_collection("products_collection")


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "product_name": product["product_name"],
        "ingredient_key": product["ingredient_key"],
        "brand_key": product["brand_key"],
        "category_key": product["category_key"],
        "quantity_key": product["quantity"],
        "calories": product["calories"],
        "eco": product["eco"],
        "bio": product["bio"],
    }


# Retrieve all products present in the database
async def retrieve_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products


# Retrieve a product with a matching ID
async def retrieve_product(_id: str) -> dict:
    product = await product_collection.find_one({"_id": ObjectId(_id)})
    if product:
        return product_helper(product)


# Add a new product into to the database
async def add_product(product_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    result.status = True

    # Check if the ingredient_key exists in the database
    ingredient_key = product_data.get("ingredient_key")
    result = await check_pk_in_collection(object_type="ingredient", object_id=ingredient_key, result=result)
    # if not await ingredient_collection.find_one({"_id": ingredient_key}):
    #     result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
    #     result.status = False
    #     return result

    # Check if the brand_key exists in the database
    brand_key = product_data.get("brand_key")
    result = await check_pk_in_collection(object_type="brand", object_id=brand_key, result=result)
    # if not await brand_collection.find_one({"_id": brand_key}):
    #     result.error_message.append("The Category {} doesn't exists in the database".format(brand_key))
    #     result.status = False
    #     return result

    # Check if the category_key exists in the database
    category_key = product_data.get("category_key")
    result = await check_pk_in_collection(object_type="category", object_id=category_key, result=result)
    # if not await category_collection.find_one({"_id": category_key}):
    #     result.error_message.append("The category_key {} doesn't exists in the database".format(category_key))
    #     result.status = False
    #     return result

    if not result.status:
        return result
    # Adding the product into the database
    try:
        product = await product_collection.insert_one(product_data)
        new_product = await product_collection.find_one({"_id": product.inserted_id})
        result.data = product_helper(new_product)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Product '{}' already exists in the database!".format(product_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a product with a matching ID
async def update_product(_id: str, product_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(product_data, result)
    if not result.status:
        return result

    # Check if the product exists
    result = await check_pk_in_collection(object_type="product", object_id=ObjectId(_id), result=result)
    # if not await product_collection.find_one({"_id": ObjectId(id)}):
    #     result.error_message.append("Product id {} doesn't exist in the database.".format(id))
    #     result.status = False
    #     return result

    # Check if the ingredient_key exists in the database
    ingredient_key = product_data.get("ingredient_key")
    result = await check_pk_in_collection(object_type="ingredient", object_id=ingredient_key, result=result)

    # if not await ingredient_collection.find_one({"ingredient_key": ingredient_key}):
    #     result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
    #     result.status = False
    #     return result

    brand_key = product_data.get("brand_key")
    result = await check_pk_in_collection(object_type="brand", object_id=brand_key, result=result)
    # if not await brand_collection.find_one({"_id": brand_key}):
    #     result.error_message.append("The brand_key {} doesn't exists in the database".format(ingredient_key))
    #     result.status = False
    #     return result

    # Check if the category_key exists in the database
    category_key = product_data.get("category_key")
    result = await check_pk_in_collection(object_type="category", object_id=category_key, result=result)
    # if not await category_collection.find_one({"_id": category_key}):
    #     result.error_message.append("The category_key {} doesn't exists in the database".format(category_key))
    #     result.error_message.append("The category_key {} doesn't exists in the database".format(category_key))
    #     result.status = False
    #     return result

    if not result.status:
        return result
    # Update the product
    updated_product = await product_collection.update_one(
        {"_id": ObjectId(_id)}, {"$set": product_data}
    )
    if updated_product:
        result.status = True
        product_updated = await product_collection.find_one({"_id": ObjectId(_id)})
        result.data = product_helper(product_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the product with id {} into the database".format(_id))
    return result


async def delete_product(_id: str):
    # Delete a product from the database
    result = ResultGeneric()
    result.status = True

    # Delete product
    if await product_collection.find_one({"_id": _id}):
        await product_collection.delete_one({"_id": _id})
        result.status = True
        return result
    else:
        result.status = False
        result.error_message.append("Couldn't find the product ID to delete")

