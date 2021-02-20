from bson import ObjectId

from app.core.database import ResultGeneric


is_object_id_map_dict = {
  "brand": False,
  "category": False,
  "company": False,
  "ingredient": False,
  "product": True,
  "recipe": True,
  "supermarket_local": False,
}


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
    :param object_type: str
        Class, object, table or collection from where is checked
    :param object_id:
        Id name of the element to be checked
    :param result:

    Returns:
    -------
    :return ResultGeneric().reset()
        A result generic object

    """

    my_dict = {
        'collection': object_type + "_collection",
        'key_name': object_type + "_key",
        'import_from_list': "app.core.logic." + object_type
    }

    _module = __import__(my_dict['import_from_list'], globals(), locals(), my_dict['collection'], 0)
    _collection = getattr(_module, my_dict['collection'])
    _is_obj_id = is_object_id_map_dict[object_type]

    if _is_obj_id:
        object_id = ObjectId(object_id)

    if not await _collection.find_one({"_id": object_id}):
        result.error_message.append("The {} '{}' doesn't exist in the database".format(object_type, object_id))
        result.status = False
        return result
    else:
        return result


async def delete_item_from_collection(_id: str, collection):
    """
    A generic function that deletes an item from the database.

    Parameters
    -------
    :param is_object_id: boolean to consider whether the PK is of the collection is of type ObjectId
    :param _id: str
        Identification name, unique, that will find in order to delete the item.
    :param collection:
        Collection  from the database where to find the item to delete.

    Returns:
    ------
    :return result: ResultGeneric()
        A result generic object
    """
    result = ResultGeneric().reset()
    result.status = True

    object_name = collection.name[:-11]
    _is_obj_id = is_object_id_map_dict[object_name]

    if _is_obj_id:
        _id = ObjectId(_id)

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
    :param is_object_id: boolean to consider whether the PK is of the collection is of type ObjectId
    :param _id: str
        Identification name, unique, that will find in order to get the item.
    :param collection:
        Collection  from the database where to find the item to get.

    Returns:
    ------
    result: ResultGeneric()
        A result generic object
    """
    result = ResultGeneric().reset()
    result.status = True

    object_name = collection.name[:-11]
    _is_obj_id = is_object_id_map_dict[object_name]

    if _is_obj_id:
        _id = ObjectId(_id)

    result.data = await collection.find_one({"_id": _id})

    if not result.data:
        result.status = False
        result.error_message.append("Couldn't find the ID '" + str(_id) + "' in the " + collection.name + ".")
    return result
