from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder

from app.core.logic.company import (
    retrieve_company,
    retrieve_companies,
    update_company, add_company, delete_company,
)
from app.core.models.company import CompanySchema, UpdateCompanyModel
from app.core.models.model_base import ResponseModel, ErrorResponseModel

company_router = APIRouter()


@company_router.get("/", response_description="Companies retrieved")
async def get_companies():
    companies = await retrieve_companies()
    if companies:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Companies data retrieved successfully",
            data=companies
        )
    return ResponseModel(
        code=status.HTTP_200_OK,
        message="Empty list returned",
        data=companies
    )


@company_router.post("/",)
async def add_company_data(company: CompanySchema = Body(...)):
    company = jsonable_encoder(company)
    new_company = await add_company(company)
    if new_company.status:
        return ResponseModel(
            code=status.HTTP_201_CREATED,
            message="Company added successfully.",
            data=new_company.data,
            )
    else:
        return ErrorResponseModel(
            code=status.HTTP_400_BAD_REQUEST,
            error_message=new_company.error_message,
        )


@company_router.get("/{id}", response_description="Company data retrieved")
async def get_company_data(id: str):
    company = await retrieve_company(id)
    if company:
        return ResponseModel(
            code=status.HTTP_200_OK,
            data=company,
            message="Company data retrieved successfully"
        )
    return ErrorResponseModel(
        code=status.HTTP_404_NOT_FOUND,
        error_message="Company '{}' doesn't exist.".format(id),
    )


@company_router.put("/{id}")
async def update_company_data(id: str, req: UpdateCompanyModel = Body(...)):
    # Update Req dictionary by filtering the "None" values
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_company = await update_company(id, req)

    if updated_company.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Company with ID: {} name update is successful".format(id),
            data=updated_company.data
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=updated_company.error_message,
    )


@company_router.delete("/{id}", response_description="Company data deleted from the database")
async def delete_company_data(id: str):
    deleted_company = await delete_company(id)
    if deleted_company.status:
        return ResponseModel(
            code=status.HTTP_200_OK,
            message="Company with ID: {} removed".format(id),
        )
    return ErrorResponseModel(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_message=deleted_company.error_message
    )
