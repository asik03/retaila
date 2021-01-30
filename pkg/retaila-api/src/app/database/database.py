import motor.motor_asyncio

from decouple import config

CLUSTER_NAME = 'cluster0'
DB_NAME = config('DB_NAME')
USER_PASSWORD = config('USER_PASSWORD')
USER_NAME = config('USER_NAME')

MONGO_DETAILS = "mongodb+srv://" + USER_NAME + ":" + USER_PASSWORD + "@" + CLUSTER_NAME + ".sqvfu.mongodb.net/" + DB_NAME + "?retryWrites=true" \
                                                                                                  "&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.Retaila


# helpers
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
        "ingredient_key": ingredient["ingredient_key"],
    }
