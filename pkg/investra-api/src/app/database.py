import motor.motor_asyncio
from bson.objectid import ObjectId

from decouple import config

DB_NAME = config('DB_NAME')
DB_PASSWORD = config('DB_PASSWORD')

MONGO_DETAILS = "mongodb+srv://Investra:" + DB_PASSWORD + "@cluster0.m54ev.mongodb.net/" + DB_NAME + "?retryWrites=true" \
                                                                                                  "&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.Investra

recipe_collection = database.get_collection("recipes_collection")


# helpers


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "recipe_name": recipe["recipe_name"],
        "ingredients": recipe["ingredients"],
        "steps": recipe["steps"],
        "extra_notes": recipe["extra_notes"],
    }


# Retrieve all recipes present in the database
async def retrieve_recipes():
    recipes = []
    async for recipe in recipe_collection.find():
        recipes.append(recipe_helper(recipe))
    return recipes


# Add a new recipe into to the database
async def add_recipe(recipe_data: dict) -> dict:
    recipe = await recipe_collection.insert_one(recipe_data)
    new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
    return recipe_helper(new_recipe)


# Retrieve a recipe with a matching ID
async def retrieve_recipe(id: str) -> dict:
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        return recipe_helper(recipe)


# Update a recipe with a matching ID
async def update_recipe(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)}) # TODO: check that id has a proper format
    if recipe:
        updated_recipe = await recipe_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recipe:
            return True
        return False


# Delete a recipe from the database
async def delete_recipe(id: str):
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        await recipe_collection.delete_one({"_id": ObjectId(id)})
        return True
