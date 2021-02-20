from test.v1.test_main import client

test_existing_company_id = "Mercadona"
test_nonexistent_company_id = "NoMercadona"

company_data_1 = {
    "_id": test_existing_company_id,
}

company_data_2 = {
    "_id": test_nonexistent_company_id,
}


def test_read_company():
    response = client.get("/company/" + test_existing_company_id)
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Company data retrieved successfully",
        "data": [
            {
                "id": test_existing_company_id,
            }
        ]
    }


def test_read_nonexistent_company():
    response = client.get("/company/" + test_nonexistent_company_id)
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "An error occurred.",
        "error_message": "Company '{}' doesn't exist.".format(test_nonexistent_company_id)
    }


def test_create_company():
    response = client.post(
        "/company/",
        json=company_data_2,
    )
    assert response.status_code == 201
    assert response.json() == {
      "code": 201,
      "message": "Company added successfully.",
      "data": [
        {
          "id": test_nonexistent_company_id,
        }
      ]
    }


def test_create_existing_company():
    response = client.post(
        "/company/",
        json=company_data_1,
    )
    assert response.status_code == 400
    assert response.json() == {
        "code": 400,
        "message": "An error occurred.",
        "error_message": [
            "Company '" + test_existing_company_id + "' already exists in the database!"
        ]
    }


def test_delete_company():
    response = client.delete(
        "/company/" + test_nonexistent_company_id,
    )
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Company with ID: " + test_nonexistent_company_id + " removed",
        "data": [
            ""
        ]
    }


def test_delete_nonexistent_company():
    response = client.delete(
        "/company/" + test_nonexistent_company_id
    )
    assert response.status_code == 422
    assert response.json() == {
      "code": 422,
      "message": "An error occurred.",
      "error_message": [
        "Couldn't find the ID '" + test_nonexistent_company_id + "' in the company_collection to delete."
      ]
    }
