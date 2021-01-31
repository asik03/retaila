from bson import ObjectId

from src.app.database.database import database, ingredient_helper, ResultGeneric

ingredient_collection = database.get_collection("ingredients_collection")


# Retrieve all ingredients present in the database
async def retrieve_ingredients():
    ingredients = []
    async for ingredient in ingredient_collection.find():
        ingredients.append(ingredient_helper(ingredient))
    return ingredients


# Retrieve a ingredient with a matching ID
async def retrieve_ingredient(id: str) -> dict:
    ingredient = await ingredient_collection.find_one({"_id": ObjectId(id)})
    if ingredient:
        return ingredient_helper(ingredient)


# Add a new ingredient into to the database
async def add_ingredient(ingredient_data: dict) -> ResultGeneric:
    result = ResultGeneric()
    ingredient_key = ingredient_data.get("ingredient_key")
    if ingredient_collection.find_one({"ingredient_key": ingredient_key}):
        result.error_message = "Ingredient_key {} already exists in the database!".format(ingredient_key)
        result.status = False
        return result
    else:
        ingredient = await ingredient_collection.insert_one(ingredient_data)
        new_ingredient = await ingredient_collection.find_one({"_id": ingredient.inserted_id})
        result.data = ingredient_helper(new_ingredient)
        result.status = True
        return result


# Update a ingredient with a matching ID
async def update_ingredient(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    ingredient = await ingredient_collection.find_one({"_id": ObjectId(id)})
    if ingredient:
        updated_ingredient = await ingredient_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_ingredient:
            return True
        return False


# Delete a ingredient from the database
async def delete_ingredient(id: str):
    ingredient = await ingredient_collection.find_one({"_id": ObjectId(id)})
    if ingredient:
        await ingredient_collection.delete_one({"_id": ObjectId(id)})
        return True
