# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional
from pydantic import BaseModel, Field


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class IngredientSchema(BaseModel):
    ingredient_key: str
    # TODO: add future fields

    class Config:
        schema_extra = {
            "example": {
                "ingredient_key": "pasta_macaroni",
            }
        }


class UpdateIngredientModel(BaseModel):
    ingredient_key: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "ingredient_key": "pasta_tagliatelle",
            }
        }
