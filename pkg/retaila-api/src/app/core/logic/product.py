from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.core.database import ResultGeneric, database
from app.core.utils import check_empty_body_request, check_pk_in_collection, delete_item_from_collection, \
    get_item_from_collection

product_collection = database.get_collection("products_collection")


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "product_name": product["product_name"],
        "ingredient_key": product["ingredient_key"],
        "brand_key": product["brand_key"],
        "category_key": product["category_key"],
        "quantity": product["quantity"],
        "calories": product["calories"],
        "eco": product["eco"],
        "bio": product["bio"],
    }


# Retrieve all products present in the core
async def retrieve_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products


# Retrieve a product with a matching ID
async def retrieve_product(_id: str) -> dict:
    product = await get_item_from_collection(_id=_id, collection=product_collection)
    if product.status:
        return product_helper(product.data)


# Add a new product into to the core
async def add_product(product_data: dict) -> ResultGeneric:
    result = ResultGeneric().reset()
    result.status = True

    # Check if the ingredient_key exists in the core
    ingredient_key = product_data.get("ingredient_key")
    result = await check_pk_in_collection(object_type="ingredient", object_id=ingredient_key, result=result)

    # Check if the brand_key exists in the core
    brand_key = product_data.get("brand_key")
    result = await check_pk_in_collection(object_type="brand", object_id=brand_key, result=result)

    # Check if the category_key exists in the core
    category_key = product_data.get("category_key")
    result = await check_pk_in_collection(object_type="category", object_id=category_key, result=result)

    if not result.status:
        return result
    # Adding the product into the core
    try:
        product = await product_collection.insert_one(product_data)
        new_product = await product_collection.find_one({"_id": product.inserted_id})
        result.data = product_helper(new_product)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Product '{}' already exists in the core!".format(product_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a product with a matching ID
async def update_product(_id: str, product_data: dict):
    result = ResultGeneric().reset()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(product_data, result)
    if not result.status:
        return result

    # Check if the product exists
    result = await check_pk_in_collection(object_type="product", object_id=_id, result=result)

    # Check if the ingredient_key exists in the core
    ingredient_key = product_data.get("ingredient_key")
    result = await check_pk_in_collection(object_type="ingredient", object_id=ingredient_key, result=result)

    brand_key = product_data.get("brand_key")
    result = await check_pk_in_collection(object_type="brand", object_id=brand_key, result=result)

    # Check if the category_key exists in the core
    category_key = product_data.get("category_key")
    result = await check_pk_in_collection(object_type="category", object_id=category_key, result=result)

    if not result.status:
        return result

    # Update the product
    updated_product = await product_collection.update_one(
        {"_id": _id}, {"$set": product_data}
    )
    if updated_product:
        result.status = True
        product_updated = await product_collection.find_one({"_id": _id})
        result.data = product_helper(product_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the product with id {} into the core".format(_id))
    return result


# Delete a product from the core
async def delete_product(_id: str):
    return await delete_item_from_collection(_id=_id, collection=product_collection)

