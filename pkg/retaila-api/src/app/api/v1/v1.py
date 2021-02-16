from decouple import config
from fastapi import APIRouter, FastAPI

from app.api.v1.routes.brand import brand_router
from app.api.v1.routes.category import category_router
from app.api.v1.routes.ingredient import ingredient_router
from app.api.v1.routes.product import product_router
from app.api.v1.routes.recipe import recipe_router

api_v1 = FastAPI(title=config("PROJECT_NAME"))


router = APIRouter()

api_v1.include_router(brand_router, tags=["Brand"], prefix="/brand")
api_v1.include_router(category_router, tags=["Category"], prefix="/category")
api_v1.include_router(ingredient_router, tags=["Ingredient"], prefix="/ingredient")
api_v1.include_router(product_router, tags=["Product"], prefix="/product")
api_v1.include_router(recipe_router, tags=["Recipe"], prefix="/recipe")


# Tags are identifiers used to group api. Routes with the same tags are grouped into a section on the API
# documentation.
@api_v1.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to " + config("PROJECT_NAME") + " API!!."}


@api_v1.get("/health", tags=["health"])
async def read_root() -> dict:
    return {"ping": "pong!"}


