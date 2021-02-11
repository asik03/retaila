# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional

from pydantic import BaseModel, Field


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class CategorySchema(BaseModel):
    category_id: str = Field(alias="_id", description="Category id")

    class Config:
        schema_extra = {
            "example": {
                "category_id": "pasta",
            }
        }


class UpdateIngredientModel(BaseModel):
    category_id: str = Field(alias="_id", description="Brand id")

    class Config:
        schema_extra = {
            "example": {
                "category_id": "pasta",
            }
        }
