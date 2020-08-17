import logging
import json

# This file is for configurations

# logger settings - basic configuration
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
log = logging.getLogger("face_api")


def final_response(code=0, message="OK", result=None):
    """
    :param code: HTTP code
    :param message: OK/General ERROR
    :param result: results object (dict)
    :return: JSON object
    """
    if result is None:
        result = {}
    return json.dumps({
        "code": code,
        "message": message,
        "result": result
    })


face_request_schema = {

    "type": "object",
    "properties": {
        "images": {"type": "array"}
    },
    "required": ["images"],
    "additionalProperties": False
}
