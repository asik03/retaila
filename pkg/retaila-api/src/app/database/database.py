import motor.motor_asyncio

from decouple import config

CLUSTER_NAME = 'cluster0'
DB_NAME = config('DB_NAME')
USER_PASSWORD = config('USER_PASSWORD')
USER_NAME = config('USER_NAME')

MONGO_DETAILS = "mongodb+srv://" + USER_NAME + ":" + USER_PASSWORD + "@" + CLUSTER_NAME + ".sqvfu.mongodb.net/" + \
                DB_NAME + "?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.Retaila


# Utils classes
class ResultGeneric:
    def __init__(self):
        self.status = False
        self.code = None
        self.data = None
        self.error_message = []


# Utils functions
def check_empty_body_request(data, result):
    # Check if an empty request body is sent.
    if len(data) < 1:
        result.status = False
        result.error_message.append("An empty request body is sent")
    else:
        result.status = True

    return result
