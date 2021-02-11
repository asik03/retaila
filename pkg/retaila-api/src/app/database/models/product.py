# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, Schema


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class ProductSchema(BaseModel):
    product_name: str
    ingredient_key: str  # Ingredient name registered in the database
    brand: str  # TODO: check if exist brand
    category: str  # TODO: check if exist category
    quantity: int  # In grams
    calories: int  # KCalories per 100gr
    eco: bool = False  # Not needed, False by default
    bio: bool = False  # Not needed, False by default
    co2_footprint: int = None  # Not needed, None by default

    class Config:
        schema_extra = {
            "example": {
                "product_name": "Macaroni Barila 500gr",
                "ingredient_key": "pasta_macaroni",
                "brand": "Barila",
                "category": "pasta",
                "quantity": 500,
                "calories": 354,
                "eco": False,
                "bio": True,
            }
        }


class UpdateProductModel(BaseModel):
    product_name: Optional[str]
    ingredient_key: Optional[str]  # Ingredient name registered in the database
    brand: Optional[str]  # TODO: check if exist brand
    category: Optional[str]  # TODO: check if exist category
    quantity: Optional[int]  # In grams
    calories: Optional[int]  # KCalories per 100gr
    eco: bool = Optional[False]  # Not needed, False by default
    bio: bool = Optional[False]  # Not needed, False by default
    co2_footprint: Optional[int] = None  # Not needed, None by default

    class Config:
        schema_extra = {
            "example": {
                "product_name": "Macaroni Barila 500gr",
                "ingredient_key": "pasta_macaroni",
                "brand": "Barila",
                "category": "pasta",
                "quantity": 500,
                "calories": 600,
                "eco": False,
                "bio": True,
            }
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