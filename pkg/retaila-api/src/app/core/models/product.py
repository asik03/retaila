# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional
from pydantic import BaseModel


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class ProductSchema(BaseModel):
    product_name: str
    ingredient_key: str  # Ingredient name registered in the core
    brand_key: str
    category_key: str
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
                "brand_key": "Barila",
                "category_key": "pasta",
                "quantity": 500,
                "calories": 354,
                "eco": False,
                "bio": True,
            }
        }


class UpdateProductModel(BaseModel):
    product_name: Optional[str]
    ingredient_key: Optional[str]  # Ingredient name registered in the core
    brand_key: Optional[str]
    category_key: Optional[str]
    quantity: Optional[int]  # In grams
    calories: Optional[int]  # KCalories per 100gr
    eco: Optional[bool] = False  # Not needed, False by default
    bio: Optional[bool] = False  # Not needed, False by default
    co2_footprint: Optional[int] = None  # Not needed, None by default

    class Config:
        schema_extra = {
            "example": {
                "product_name": "Macaroni Barila 500gr",
                "ingredient_key": "pasta_macaroni",
                "brand_key": "Barila",
                "category_key": "pasta",
                "quantity": 500,
                "calories": 600,
                "eco": False,
                "bio": True,
            }
        }

