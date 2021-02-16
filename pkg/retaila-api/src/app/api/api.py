from fastapi import FastAPI, APIRouter

# def get_application():
#     settings.initialize_settings()
#     dictConfig(log_config)
#     _app = FastAPI(title=settings.PROJECT_NAME)
#     _app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=[""],
#         allow_headers=[""],
#     )
#     _app.add_middleware(SessionMiddleware, secret_key="kanara")
#     return _app


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
from app.api.v1.v1 import api_v1

# Deprecated
api_name = "Retaila"

app = FastAPI()
app.mount("/api/v1", api_v1)





