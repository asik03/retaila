from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.routes.student import router as StudentRouter

api_name = "Investra"

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
app.include_router(StudentRouter, tags=["Student"], prefix="/student")


# Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API
# documentation.
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to " + api_name + " API!."}
