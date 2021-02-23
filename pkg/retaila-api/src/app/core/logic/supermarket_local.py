from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.core.database import database, ResultGeneric
from app.core.utils import check_empty_body_request, check_pk_in_collection, delete_item_from_collection, \
    get_item_from_collection, is_object_id_map_dict

supermarket_local_collection = database.get_collection("supermarket_local_collection")


def supermarket_local_helper(supermarket_local) -> dict:
    return {
        "id": str(supermarket_local["_id"]),
        "company_key": supermarket_local["company_key"],
        "postcode": supermarket_local["postcode"],
        "products": supermarket_local["products"],
    }


# Retrieve all supermarket_locals present in the database
async def retrieve_supermarket_locals():
    supermarket_locals = []
    async for supermarket_local in supermarket_local_collection.find():
        supermarket_locals.append(supermarket_local_helper(supermarket_local))
    return supermarket_locals


# Retrieve a supermarket_local with a matching ID
async def retrieve_supermarket_local(_id: str) -> dict:
    supermarket_local = await get_item_from_collection(
        _id=_id,
        collection=supermarket_local_collection,
    )
    if supermarket_local.status:
        return supermarket_local_helper(supermarket_local.data)


# TODO: add new product with price into a supermarket
# Add a new supermarket_local into to the database
async def add_supermarket_local(supermarket_local_data: dict) -> ResultGeneric:
    result = ResultGeneric().reset()
    result.status = True

    # Check if the company exists in the database
    company_key = supermarket_local_data.get("company_key")
    result = await check_pk_in_collection(
        object_type="company",
        _id=company_key,
        result=result,
    )

    # Check if the products of the supermarket_local exists in the database
    for product in supermarket_local_data.get("products"):
        product_key = product.get("product_key")
        result = await check_pk_in_collection(
            object_type="product",
            _id=product_key,
            result=result,
        )

    if not result.status:
        # Return to avoid the updating
        return result

    # Adding the supermarket_local into the database
    try:
        supermarket_local = await supermarket_local_collection.insert_one(supermarket_local_data)
        new_supermarket_local = await supermarket_local_collection.find_one({"_id": supermarket_local.inserted_id})
        result.data = supermarket_local_helper(new_supermarket_local)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Supermarket_local '{}' already exists in the database!".format(supermarket_local_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a supermarket_local with a matching ID
async def update_supermarket_local(_id: str, supermarket_local_data: dict):
    result = ResultGeneric().reset()
    result.status = True
    result.error_message = []

    # Check if an empty request body is sent.
    result = check_empty_body_request(supermarket_local_data, result)
    if not result.status:
        return result

    # Check if the supermarket_local exists
    result = await check_pk_in_collection(
        object_type="supermarket_local",
        _id=_id, result=result,
    )

    if not result.status:
        return result

    # Check if the company exists in the database
    company_key = supermarket_local_data.get("company_key")
    result = await check_pk_in_collection(
        object_type="company",
        _id=company_key,
        result=result,
    )

    # Check if the products of the supermarket_local exist in the database
    for product in supermarket_local_data.get("products"):
        product_key = product.get("product_key")
        result = await check_pk_in_collection(
            object_type="product",
            _id=product_key,
            result=result
        )

    if not result.status:
        # Return to avoid the updating
        return result

    # Update the supermarket_local
    updated_supermarket_local = await supermarket_local_collection.update_one(
        {"_id": ObjectId(_id)}, {"$set": supermarket_local_data}
    )
    if updated_supermarket_local:
        result.status = True
        supermarket_local_updated = await supermarket_local_collection.find_one({"_id": ObjectId(_id)})
        result.data = supermarket_local_helper(supermarket_local_updated)
    else:
        result.status = False
        result.error_message.append("There was a problem while updating the supermarket_local with id {} into the database".format(_id))
    return result


# Delete a supermarket_local from the database
async def delete_supermarket_local(_id: str):
    return await delete_item_from_collection(
        _id=_id,
        collection=supermarket_local_collection
    )







