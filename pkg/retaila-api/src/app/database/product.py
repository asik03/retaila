from bson import ObjectId

from src.app.database.brand import brand_collection
from src.app.database.category import category_collection
from src.app.database.database import ResultGeneric, database, product_helper, checkEmptyBodyRequest
from src.app.database.ingredient import ingredient_collection

product_collection = database.get_collection("products_collection")


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
    if not await ingredient_collection.find_one({"ingredient_key": ingredient_key}):
        result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
        result.status = False
        return result

    # Check if the brand_name_key exists in the database
    brand_name_key = product_data.get("brand_name_key")
    if not await brand_collection.find_one({"brand_name_key": brand_name_key}):
        result.error_message.append("The brand_name_key {} doesn't exists in the database".format(brand_name_key))
        result.status = False
        return result

    # Check if the category_key exists in the database
    category_key = product_data.get("category_key")
    if not await category_collection.find_one({"category_key": category_key}):
        result.error_message.append("The category_key {} doesn't exists in the database".format(category_key))
        result.status = False
        return result

    # Adding the product into the database
    product = await product_collection.insert_one(product_data)
    if product:
        new_product = await product_collection.find_one({"_id": product.inserted_id})
        result.status = True
        result.data = product_helper(new_product)
    else:
        result.status = False
        result.error_message.append("There was a problem while adding the product with id {} into the database".format(id))
    return result


# Update a product with a matching ID
async def update_product(id: str, product_data: dict):
    result = ResultGeneric()
    result.status = True

    # Check if an empty request body is sent.
    result = checkEmptyBodyRequest(product_data)
    if not result.status:
        return result

    # Check if the product exists
    if not await product_collection.find_one({"_id": ObjectId(id)}):
        result.error_message.append("Product id {} doesn't exist in the database.".format(id))
        result.status = False
        return result

    # Check if the ingredient_key exists in the database
    ingredient_key = product_data.get("ingredient_key")
    if not await ingredient_collection.find_one({"ingredient_key": ingredient_key}):
        result.error_message.append("The ingredient {} doesn't exists in the database".format(ingredient_key))
        result.status = False
        return result

    # Check if the brand_name_key exists in the database
    brand_name_key = product_data.get("brand_name_key")
    if not await brand_collection.find_one({"brand_name_key": brand_name_key}):
        result.error_message.append("The brand_name_key {} doesn't exists in the database".format(brand_name_key))
        result.status = False
        return result

    # Check if the category_key exists in the database
    category_key = product_data.get("category_key")
    if not await category_collection.find_one({"category_key": category_key}):
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
        result.error_message.append("There was a problem while updating the product with id {} into the database".format(id))
    return result


# Delete a product from the database
async def delete_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        await product_collection.delete_one({"_id": ObjectId(id)})
        return True
