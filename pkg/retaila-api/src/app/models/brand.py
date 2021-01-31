# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional

from pydantic import BaseModel


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class BrandSchema(BaseModel):
    brand_key: str
    super_private_brand: bool

    class Config:
        schema_extra = {
            "example": {
                "brand_key": "Barila",
                "super_private_brand": False,
            }
        }


class UpdateBrandModel(BaseModel):
    brand_key: Optional[str]
    super_private_brand: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "brand_key": "Hacendado",
                "super_private_key": True,
            }
        }