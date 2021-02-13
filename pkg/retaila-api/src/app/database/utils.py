def check_empty_body_request(data, result):
    # Check if an empty request body is sent.
    if len(data) < 1:
        result.status = False
        result.error_message.append("An empty request body is sent")
    else:
        result.status = True

    return result


async def check_pk_in_collection(object_type, object_id, result):
    """
    A function that check if exist a primary key in a foreign collection.

    Parameters
    -------
    object_type: str
        Class, object, table or collection from where is checked
    object_id:
        Id name of the element to be checked
    result: ResultGeneric()
        A result generic object
    """

    my_dict = {
        'collection': object_type + "_collection",
        'key_name': object_type + "_key",
        'import_from_list': "app.database.logic." + object_type
    }

    _module = __import__(my_dict['import_from_list'], globals(), locals(), my_dict['collection'], 0)
    _collection = getattr(_module, my_dict['collection'])
    if not await _collection.find_one({"_id": object_id}):
        result.error_message.append("The {} {} doesn't exist in the database".format(object_type, object_id))
        result.status = False
        return result
    else:
        return result
