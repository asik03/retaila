from test.v1.test_main import client

test_existing_brand_id = "Barila"
test_nonexistent_brand_id = "NoBarila"

brand_data_1 = {
    "_id": test_existing_brand_id,
    "super_private_brand": False
}

brand_data_2 = {
    "_id": test_nonexistent_brand_id,
    "super_private_brand": False
}


def test_read_brand():
    response = client.get("/brand/" + test_existing_brand_id)
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Brand data retrieved successfully",
        "data": [
            {
                "id": test_existing_brand_id,
                "super_private_brand": False
            }
        ]
    }


def test_read_nonexistent_brand():
    response = client.get("/brand/" + test_nonexistent_brand_id)
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "An error occurred.",
        "error_message": "Brand '{}' doesn't exist.".format(test_nonexistent_brand_id)
    }


def test_create_brand():
    response = client.post(
        "/brand/",
        json=brand_data_2,
    )
    assert response.status_code == 201
    assert response.json() == {
      "code": 201,
      "message": "Brand added successfully.",
      "data": [
        {
          "id": test_nonexistent_brand_id,
          "super_private_brand": False
        }
      ]
    }


def test_create_existing_brand():
    response = client.post(
        "/brand/",
        json=brand_data_1,
    )
    assert response.status_code == 400
    assert response.json() == {
        "code": 400,
        "message": "An error occurred.",
        "error_message": [
            "Brand '" + test_existing_brand_id + "' already exists in the database!"
        ]
    }


def test_delete_brand():
    response = client.delete(
        "/brand/" + test_nonexistent_brand_id,
    )
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Brand with ID: " + test_nonexistent_brand_id + " removed",
        "data": [
            ""
        ]
    }


def test_delete_nonexistent_brand():
    response = client.delete(
        "/brand/" + test_nonexistent_brand_id
    )
    assert response.status_code == 422
    assert response.json() == {
      "code": 422,
      "message": "An error occurred.",
      "error_message": [
        "Couldn't find the ID '" + test_nonexistent_brand_id + "' in the brand_collection to delete."
      ]
    }
