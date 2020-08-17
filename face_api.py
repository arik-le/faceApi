import os
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import APIErrorException
from msrest.authentication import CognitiveServicesCredentials
from urllib.request import urlopen
from config import log

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['FACE_SUBSCRIPTION_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']


class FaceApi:
    def __init__(self, images):
        try:
            self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        except APIErrorException as err:
            log.exception(err)
        self.results = {}
        self.get_most_common_face(images)

    @staticmethod
    def msg_err(err):
        return {"err": err}

    def get_results(self):
        return self.results

    def get_most_common_face(self, images: list):
        img_dict = dict()
        images_ids = list()
        try:
            for img in images:
                try:
                    img_file = urlopen(img)
                except ValueError:  # invalid URL , opening file
                    img_file = open(img, 'rb')
                try:
                    detected_faces = self.face_client.face.detect_with_stream(img_file)
                    for face in detected_faces:
                        img_dict.update({face.face_id: {"image": img, "rectangle": face.face_rectangle}})
                    images_ids = images_ids + list(map(lambda x: x.face_id, detected_faces))
                except APIErrorException as err:
                    log.exception(err)
                    if "Access denied" in err.message:
                        self.results = self.msg_err("Authentication Failed, check key or endpoint")
                        return

            sums = [0, 0, "", ""]  # all sums and values needed for results
            log.debug(f"length of all face ids:{len(images_ids)}")
            for f_id in images_ids:
                ids_w_iter_id = images_ids.copy()  # id's without the current id
                ids_w_iter_id.remove(f_id)
                try:
                    similar_faces = self.face_client.face.find_similar(face_id=f_id, face_ids=ids_w_iter_id)
                    if not similar_faces:
                        pass
                    else:
                        img_dict[f_id].update({"similar_faces": len(similar_faces)})
                except APIErrorException as err:
                    log.exception(err)
                    if "Access denied" in err.message:
                        self.results = self.msg_err("Authentication Failed, check key or endpoint")
                        return

            for f_id, face_obj in img_dict.items():
                face_size = int(face_obj['rectangle'].width) * int(face_obj['rectangle'].height)
                if 'similar_faces' in face_obj and face_obj['similar_faces'] > 0:
                    if face_obj['similar_faces'] >= sums[0] and face_size >= sums[1]:
                        sums[0] = face_obj['similar_faces']
                        sums[1] = face_size
                        sums[2] = face_obj['image']
                        sums[3] = face_obj['rectangle']

            if sums[0] > 0:
                results = {
                            "Image": sums[2],
                            "Coordinates": {
                                    "Left(X)": int(sums[3].left),
                                    "Top(Y)": int(sums[3].top),
                                    "X+Width": int(sums[3].left)+int(sums[3].width),
                                    "Y+Height": int(sums[3].top)+int(sums[3].height)
                                }
                          }
                log.debug(results)
                self.results = results

        except Exception as err:
            log.exception(err)
            self.results = self.msg_err(f"General err: {err}")
