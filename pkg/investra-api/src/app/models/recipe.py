# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, Schema


class IngredientQuantity(BaseModel):
    ingredient_key: str  # Ingredient directly, not considering the brand or any attribute.
    quantity: int


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class RecipeSchema(BaseModel):
    id: int
    ingredients: List[IngredientQuantity] = []  # Ingredients list, made of "ingredients key"
    steps: List[str] = []   # List of the steps or instructions to make the recipe.
    extra_notes: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "Pesto macaroni",
                "ingredients": [{"pasta macaroni", 200}, {"pesto sauce", 50}, {"salt", 4}],
                "steps": ["Boil the water", "Put the pasta and wait 5 mins", "Put the sauce into the pasta. Voila"],
                "extra_notes": ["It is better to wait until the water turns 90ºC"],
            }
        }


class UpdateRecipeModel(BaseModel):
    id: Optional[int]
    ingredients: Optional[List[IngredientQuantity]] = []  # Ingredients list, made of "ingredients key"
    steps: Optional[List[str]] = []  # List of the steps or instructions to make the recipe.
    extra_notes: Optional[List[str]] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "Pesto macaroni",
                "ingredients": [{"pasta macaroni", 200}, {"pesto sauce", 50}, {"salt", 4}],
                "steps": ["Boil the water", "Put the pasta and wait 5 mins", "Put the sauce into the pasta. Voila"],
                "extra_notes": ["It is better to wait until the water turns 90ºC"],
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
