from pymongo.errors import DuplicateKeyError
from app.core.database import database, ResultGeneric
from app.core.utils import check_empty_body_request, check_pk_in_collection, delete_item_from_collection, \
    get_item_from_collection, is_object_id_map_dict

company_collection = database.get_collection("company_collection")

def company_helper(company) -> dict:
    return {
        "id": str(company["_id"]),
    }


# Retrieve all companies present in the database
async def retrieve_companies():
    companies = []
    async for company in company_collection.find():
        companies.append(company_helper(company))
    return companies


# Retrieve a company with a matching ID
async def retrieve_company(_id: str) -> dict:
    company = await get_item_from_collection(_id=_id, collection=company_collection)
    if company.status:
        return company_helper(company.data)


# Add a new company into to the database
async def add_company(company_data: dict) -> ResultGeneric:
    result = ResultGeneric().reset()
    result.status = True

    try:
        company = await company_collection.insert_one(company_data)
        new_company = await company_collection.find_one({"_id": company.inserted_id})
        result.data = company_helper(new_company)
        result.status = True
    except DuplicateKeyError:
        result.error_message.append("Company '{}' already exists in the database!".format(company_data.get("_id")))
        result.status = False
    except BaseException:
        result.error_message.append("Unrecognized error")
        result.status = False

    return result


# Update a company with a matching ID
async def update_company(_id: str, company_data: dict):
    result = ResultGeneric().reset()
    result.status = True

    # Check if an empty request body is sent.
    result = check_empty_body_request(company_data, result)
    if not result.status:
        return result

    # Check if the company exists
    result = await check_pk_in_collection(object_type="company", _id=_id, result=result)
    if not result.status:
        return result

    # Update the company
    updated_company = await company_collection.update_one(
        {"_id": _id}, {"$set": company_data}
    )
    if updated_company:
        result.status = True
        company_updated = await company_collection.find_one({"_id": _id})
        result.data = company_helper(company_updated)
    else:
        result.status = False
        result.error_message.append(
            "There was a problem while updating the company with id {} into the database".format(_id)
        )
    return result


# Delete a company from the database
async def delete_company(_id: str):
    return await delete_item_from_collection(_id=_id, collection=company_collection)
