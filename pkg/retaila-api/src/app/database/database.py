import motor.motor_asyncio

from decouple import config

CLUSTER_NAME = 'cluster0'
DB_NAME = config('DB_NAME')
USER_PASSWORD = config('USER_PASSWORD')
USER_NAME = config('USER_NAME')

MONGO_DETAILS = "mongodb+srv://" + USER_NAME + ":" + USER_PASSWORD + "@" + CLUSTER_NAME + ".sqvfu.mongodb.net/" + \
                DB_NAME + "?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.Retaila


# helpers
def brand_helper(brand) -> dict:
    print(str(brand))
    return {
        "id": str(brand["_id"]),
        "super_private_brand": brand["super_private_brand"],
    }


def category_helper(category) -> dict:
    return {
        "id": str(category["_id"]),
    }


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "recipe_name": recipe["recipe_name"],
        "ingredients": recipe["ingredients"],
        "steps": recipe["steps"],
        "extra_notes": recipe["extra_notes"],
    }


def ingredient_helper(ingredient) -> dict:
    return {
        "id": str(ingredient["_id"]),
    }


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "product_name": product["product_name"],
        "ingredient_key": product["ingredient_key"],
        "brand": product["brand"],
        "category": product["category"],
        "quantity": product["quantity"],
        "calories": product["calories"],
        "eco": product["eco"],
        "bio": product["bio"],

    }


# Utils classes
class ResultGeneric:
    data = None
    status = False
    error_message = []


# Utils functions
def checkEmptyBodyRequest(data):
    result = ResultGeneric()
    # Check if an empty request body is sent.
    if len(data) < 1:
        result.status = False
        result.error_message.append("An empty request body is sent")
    else:
        result.status = True

    return result
