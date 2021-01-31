# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional

from pydantic import BaseModel


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class CategorySchema(BaseModel):
    category_key: str

    class Config:
        schema_extra = {
            "example": {
                "category_key": "pasta",
            }
        }


class UpdateIngredientModel(BaseModel):
    category_key: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "category_key": "pasta",
            }
        }
