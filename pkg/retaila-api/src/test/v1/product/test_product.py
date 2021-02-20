from test.v1.test_main import client

test_existing_ingredient_key = "pasta_macaroni"
test_nonexistent_ingredient_key = "no_pasta_macaroni"

test_existent_brand_key = "Barila"
test_nonexistent_brand_key = "NoBarila"

test_existent_category_key = "pasta"
test_nonexistent_category_key = "noPasta"


'''
NOTES
- ingredient_key needs to exist in the collection
- brand_key needs to exist in the collection
- category_key needs to exist in the collection
'''
product_data_1 = {
    "product_name": "Macaroni Barila 500gr",
    "ingredient_key": test_existing_ingredient_key,
    "brand_key": test_existent_brand_key,
    "category_key": test_existent_category_key,
    "quantity": 500,
    "calories": 354,
    "eco": False,
    "bio": True
}


'''
NOTES
- ingredient_key needs to exist in the collection
- brand_key needs to not exist in the collection
- category_key needs to exist in the collection
'''
product_data_2 = {
    "product_name": "Macaroni Barila 500gr",
    "ingredient_key": test_nonexistent_ingredient_key,
    "brand_key": test_nonexistent_brand_key,
    "category_key": test_nonexistent_category_key,
    "quantity": 500,
    "calories": 354,
    "eco": False,
    "bio": True}


# def test_read_product():
#     response = client.get("/product/" + test_existing_product_id)
#     assert response.status_code == 200
#     assert response.json() == {
#         "code": 200,
#         "message": "Product data retrieved successfully",
#         "data": [
#             {
#                 "id": test_existing_product_id,
#             }
#         ]
#     }

#
# def test_read_nonexistent_product():
#     response = client.get("/product/" + test_nonexistent_product_id)
#     assert response.status_code == 404
#     assert response.json() == {
#         "code": 404,
#         "message": "An error occurred.",
#         "error_message": "Product doesn't exist."
#     }


# def test_create_product():
#     response = client.post(
#         "/product/",
#         json=product_data_2,
#     )
#     assert response.status_code == 201
#     assert response.json() == {
#       "code": 201,
#       "message": "Product added successfully.",
#       "data": [
#         {
#           "id": test_nonexistent_product_id,
#         }
#       ]
#     }


# def test_create_existing_product():
#     response = client.post(
#         "/product/",
#         json=product_data_1,
#     )
#     assert response.status_code == 400
#     assert response.json() == {
#         "code": 400,
#         "message": "An error occurred.",
#         "error_message": [
#             "Product '" + test_existing_product_id + "' already exists in the database!"
#         ]
#     }

#
# def test_delete_product():
#     response = client.delete(
#         "/product/" + test_nonexistent_product_id,
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "code": 200,
#         "message": "Product with ID: " + test_nonexistent_product_id + " removed",
#         "data": [
#             ""
#         ]
#     }


# def test_delete_nonexistent_product():
#     response = client.delete(
#         "/product/" + test_nonexistent_product_id
#     )
#     assert response.status_code == 422
#     assert response.json() == {
#       "code": 422,
#       "message": "An error occurred.",
#       "error_message": [
#         "Couldn't find the ID '" + test_nonexistent_product_id + "' in the products_collection to delete."
#       ]
#     }
