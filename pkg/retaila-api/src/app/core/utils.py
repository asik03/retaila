from app.core.database import ResultGeneric


def check_empty_body_request(data, result):
    # Check if an empty request body is sent.
    if len(data) < 1:
        result.status = False
        result.error_message.append("An empty request body is sent")
    else:
        result.status = True

    return result


async def check_pk_in_collection(object_type, object_id, result):
    """A function that check if exist a primary key in a foreign collection.

    Parameters
    -------
    object_type: str
        Class, object, table or collection from where is checked
    object_id:
        Id name of the element to be checked

    Returns:
    -------
    result: ResultGeneric().reset()
        A result generic object
    """

    my_dict = {
        'collection': object_type + "_collection",
        'key_name': object_type + "_key",
        'import_from_list': "app.core.logic." + object_type
    }

    _module = __import__(my_dict['import_from_list'], globals(), locals(), my_dict['collection'], 0)
    _collection = getattr(_module, my_dict['collection'])
    if not await _collection.find_one({"_id": object_id}):
        result.error_message.append("The {} {} doesn't exist in the database".format(object_type, object_id))
        result.status = False
        return result
    else:
        return result


async def delete_item_from_collection(_id: str, collection):
    """
    A generic function that deletes an item from the database.

    Parameters
    -------
    _id: str
        Identification name, unique, that will find in order to delete the item.
    collection:
        Collection  from the database where to find the item to delete.

    Returns:
    ------
    result: ResultGeneric()
        A result generic object
    """
    result = ResultGeneric().reset()
    result.status = True

    if await collection.find_one({"_id": _id}):
        await collection.delete_one({"_id": _id})
        result.status = True
    else:
        result.status = False
        result.error_message.append("Couldn't find the ID '" + str(_id) + "' in the " + collection.name + " to delete.")
    return result


async def get_item_from_collection(_id: str, collection):
    """
    A generic function that gets an item from the database.

    Parameters
    -------
    _id: str
        Identification name, unique, that will find in order to get the item.
    collection:
        Collection  from the database where to find the item to get.

    Returns:
    ------
    result: ResultGeneric()
        A result generic object
    """
    result = ResultGeneric().reset()
    result.status = True
    result.data = await collection.find_one({"_id": _id})

    if not result.data:
        result.status = False
        result.error_message.append("Couldn't find the ID '" + str(_id) + "' in the " + collection.name + ".")
    return result
