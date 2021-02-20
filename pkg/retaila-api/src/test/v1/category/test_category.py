from test.v1.test_main import client

test_existing_category_id = "pasta"
test_nonexistent_category_id = "Caca"

category_data_1 = {
    "_id": test_existing_category_id,
}

category_data_2 = {
    "_id": test_nonexistent_category_id,
}


def test_read_category():
    response = client.get("/category/" + test_existing_category_id)
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Category data retrieved successfully",
        "data": [
            {
                "id": test_existing_category_id,
            }
        ]
    }


def test_read_nonexistent_category():
    response = client.get("/category/" + test_nonexistent_category_id)
    assert response.status_code == 404
    assert response.json() == {
        "code": 404,
        "message": "An error occurred.",
        "error_message": "Category '{}' doesn't exist.".format(test_nonexistent_category_id)
    }


def test_create_category():
    response = client.post(
        "/category/",
        json=category_data_2,
    )
    assert response.status_code == 201
    assert response.json() == {
      "code": 201,
      "message": "Category added successfully.",
      "data": [
        {
          "id": test_nonexistent_category_id,
        }
      ]
    }


def test_create_existing_category():
    response = client.post(
        "/category/",
        json=category_data_1,
    )
    assert response.status_code == 400
    assert response.json() == {
        "code": 400,
        "message": "An error occurred.",
        "error_message": [
            "Category '" + test_existing_category_id + "' already exists in the database!"
        ]
    }


def test_delete_category():
    response = client.delete(
        "/category/" + test_nonexistent_category_id,
    )
    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Category with ID: " + test_nonexistent_category_id + " removed",
        "data": [
            ""
        ]
    }


def test_delete_nonexistent_category():
    response = client.delete(
        "/category/" + test_nonexistent_category_id
    )
    assert response.status_code == 422
    assert response.json() == {
      "code": 422,
      "message": "An error occurred.",
      "error_message": [
        "Couldn't find the ID '" + test_nonexistent_category_id + "' in the category_collection to delete."
      ]
    }
