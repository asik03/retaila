# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional

from pydantic import BaseModel, Field


def brand_helper(brand) -> dict:
    print(str(brand))
    return {
        "id": str(brand["_id"]),
        "super_private_brand": brand["super_private_brand"],
    }


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class BrandSchema(BaseModel):
    brand_id: str = Field(alias="_id", description="Brand id")
    super_private_brand: bool

    class Config:
        schema_extra = {
            "example": {
                "_id": "Barila",
                "super_private_brand": False,
            }
        }


class UpdateBrandModel(BaseModel):
    id: str = Field(alias="_id", description="Brand id")
    super_private_brand: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "_id": "Hacendado",
                "super_private_key": True,
            }
        }

