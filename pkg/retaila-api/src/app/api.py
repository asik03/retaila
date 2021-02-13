from fastapi import FastAPI, APIRouter

from app.routes.brand import brand_router
from app.routes.category import category_router
from app.routes.ingredient import ingredient_router
from app.routes.product import product_router
from app.routes.recipe import recipe_router

api_name = "Retaila"

# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


app = FastAPI()
router = APIRouter()

app.include_router(brand_router, tags=["Brand"], prefix="/brand")
app.include_router(category_router, tags=["Category"], prefix="/category")
app.include_router(ingredient_router, tags=["Ingredient"], prefix="/ingredient")
app.include_router(product_router, tags=["Product"], prefix="/product")
app.include_router(recipe_router, tags=["Recipe"], prefix="/recipe")


# Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API
# documentation.
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to " + api_name + " API!!."}


@app.get("/health", tags=["health"])
async def read_root() -> dict:
    return {"ping": "pong!"}
