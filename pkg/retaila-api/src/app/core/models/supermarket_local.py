# Pydantic Schema's are used for validating data along with serializing (JSON -> Python) and de-serializing (Python
# -> JSON). It does not serve as a Mongo schema validator, in other words.

from typing import Optional, List
from pydantic import BaseModel


class Price(BaseModel):
    value: float
    currency: str # EUR, USD, etc


class ProductPrice(BaseModel):
    product_key: str
    price: Price


# ellipsis "..." means that the Field is required. It could be replaced with None or a default value.
class SupermarketLocalSchema(BaseModel):
    company_key: str  # Company ID of the supermarket
    postcode: int
    products: List[ProductPrice] = []

    class Config:
        schema_extra = {
            "example": {
                "company_key": "Mercadona",
                "postcode": 28229,
                "products": [
                    {
                        "product_key": "Un ID UUII de esos",
                        "price": {
                            "value": 12.5,
                            "currency": "EUR"
                        }
                    },
                    {
                        "product_key": "Otro ID UUII de esos",
                        "price": {
                            "value": 1.23,
                            "currency": "EUR"
                        }
                    },
                    {
                        "product_key": "OtroMas ID UUII de esos",
                        "price": {
                            "value": 0.89,
                            "currency": "EUR"
                        }
                    },
                ],
            }
        }


class UpdateSupermarketLocalModel(BaseModel):
    company_key: Optional[str]  # Company ID of the supermarket
    postcode: Optional[int]
    products: Optional[List[ProductPrice]] = []

    class Config:
        schema_extra = {
            "example": {
                "company_key": "Mercadona",
                "postcode": 28229,
                "products": [
                    {
                        "product_key": "Un ID UUII de esos",
                        "price": {
                            "value": 11.5,
                            "currency": "EUR"
                        }
                    },
                    {
                        "product_key": "Otro ID UUII de esos",
                        "price": {
                            "value": 1.13,
                            "currency": "EUR"
                        }
                    },
                    {
                        "product_key": "OtroMas ID UUII de esos",
                        "price": {
                            "value": 0.87,
                            "currency": "EUR"
                        }
                    },
                ],
            }
        }


