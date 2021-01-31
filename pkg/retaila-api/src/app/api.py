from fastapi import FastAPI, APIRouter

from src.app.routes.ingredient import ingredient_router
from src.app.routes.recipe import recipe_router

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

app.include_router(recipe_router, tags=["Recipe"], prefix="/recipe")
app.include_router(ingredient_router, tags=["Ingredient"], prefix="/ingredient")


# Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API
# documentation.
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to " + api_name + " API!!."}
