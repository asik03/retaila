from typing import Type

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from src.app.database.logic.brand import brand_collection
from src.app.database.logic.category import category_collection
from src.app.database.database import ResultGeneric, database, check_empty_body_request
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
async def retrieve_product(id: str) -> dict:
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)


# Add a new product into to the database
async def add_product(product_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    result.status = True

    # Check if the ingredient_key exists in the database
    ingredient_key = product_data.get("ingredient_key")
    if not await ingredient_collection.find_one({"_id": ingredient_key}):
        result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
        result.status = False
        return result

    # Check if the brand_key exists in the database
    brand_key = product_data.get("brand_key")
    if not await brand_collection.find_one({"_id": brand_key}):
        result.error_message.append("The Category {} doesn't exists in the database".format(brand_key))
        result.status = False
        return result

    # Check if the category_key exists in the database
    category_key = product_data.get("category_key")
    if not await category_collection.find_one({"_id": category_key}):
        result.error_message.append("The category_key {} doesn't exists in the database".format(category_key))
        result.status = False
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

    # Adding the product into the database


# Update a product with a matching ID
async def update_product(id: str, product_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(product_data, result)
    if not result.status:
        return result

    # Check if the product exists
    if not await product_collection.find_one({"_id": ObjectId(id)}):
        result.error_message.append("Product id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # Check if the ingredient_key exists in the database
    ingredient_key = product_data.get("ingredient_key")
    # TODO: check
    result = check_value_in_other_collection(type="ingredient", id=ingredient_key, result=result)

    # if not await ingredient_collection.find_one({"ingredient_key": ingredient_key}):
    #     result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
    #     result.status = False
    #     return result


    brand_key = product_data.get("brand_key")
    if not await brand_collection.find_one({"_id": brand_key}):
        result.error_message.append("The brand_key {} doesn't exists in the database".format(ingredient_key))
        result.status = False
        return result

    # Check if the category_key exists in the database
    category_key = product_data.get("category_key")
    # result = check_value_in_other_collection(collection="category", id=category_key, result=result)
    if not await category_collection.find_one({"_id": category_key}):
        result.error_message.append("The category_key {} doesn't exists in the database".format(category_key))
        result.status = False
        return result

    # Update the product
    updated_product = await product_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": product_data}
    )
    if updated_product:
        result.status = True
        product_updated = await product_collection.find_one({"_id": ObjectId(id)})
        result.data = product_helper(product_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the product with id {} into the database".format(id))
    return result


# Delete a product from the database
async def delete_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        await product_collection.delete_one({"_id": ObjectId(id)})
        return True


# Check if exists a value of another collection
# collection: class, object, table or collection from where is checked
# id: name of the element to be checked
# result: a result generic object
def check_value_in_other_collection(type, id, result):
    my_dict = {
        'collection': [type + "_collection"],
        'key_name': type + "_key",
        'import_from_list': "src.app.database.logic." + type
    }

    _type = __import__(my_dict['import_from_list'], globals(), locals(), my_dict['collection'], 0)
    _collection = _type.ingredient_collection
    if not _collection.find_one({"_id": id}):
        result.error_message.append("The {} {} doesn't exist in the database".format(type, id))
        result.status = False
        return result
    else:
        return result
