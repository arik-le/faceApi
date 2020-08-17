from flask import Flask, request
from face_api import FaceApi
from config import log, final_response, face_request_schema
from jsonschema.exceptions import ValidationError
from jsonschema import validate

app = Flask(__name__)


# main route
@app.route("/", methods=["POST"])
def app_start():
    try:
        """
        main function for detecting similar faces between list of images
        get JSON object like:  { "images":[url/local-img,url...]
        return: JSON object with results of most common face in the best image (most largest face)
        """
        req_data = request.get_json()
        validate(instance=req_data, schema=face_request_schema)  # validate schema
        log.debug(f"Request for Face APi {req_data}")
        face_api_process = FaceApi(req_data['images'])
        return final_response(code=200, result=face_api_process.get_results())
    except ValidationError as err:
        log.error(err.validator_value)
        log.error(err.message)
        return final_response(code=400, message=err.message, result=err.validator_value)
    except Exception as err:
        log.exception(err)
        return final_response(code=500, message="General Error", result=err)


if __name__ == '__main__':
    '''
     Don't forget to open 5000 (or any other selected) port on firewall
     '''
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)
