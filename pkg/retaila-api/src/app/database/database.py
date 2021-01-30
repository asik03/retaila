import motor.motor_asyncio

from decouple import config

DB_NAME = config('DB_NAME')
DB_PASSWORD = config('DB_PASSWORD')

MONGO_DETAILS = "mongodb+srv://Investra:" + DB_PASSWORD + "@cluster0.m54ev.mongodb.net/" + DB_NAME + "?retryWrites=true" \
                                                                                                  "&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.Investra


# helpers
def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "recipe_name": recipe["recipe_name"],
        "ingredients": recipe["ingredients"],
        "steps": recipe["steps"],
        "extra_notes": recipe["extra_notes"],
    }
