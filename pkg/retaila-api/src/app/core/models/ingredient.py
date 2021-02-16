# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from pydantic import BaseModel, Field


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class IngredientSchema(BaseModel):
    ingredient_id: str = Field(alias="_id", description="Ingredient id")
    # TODO: add future fields

    class Config:
        schema_extra = {
            "example": {
                "_id": "pasta_macaroni",
            }
        }


class UpdateIngredientModel(BaseModel):
    ingredient_id: str = Field(alias="_id", description="Ingredient id")

    class Config:
        schema_extra = {
            "example": {
                "_id": "pasta_tagliatelle",
            }
        }


