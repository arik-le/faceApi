# faceApi
## Face API project

### What id does?
  * Detect Faces in Images.
  * Find Similar Faces of all the images.
  * Return the image and coordinates to the most common and largest face.

### Configurations
Before running:
  Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
  This key will serve all examples in this document.
  'FACE_SUBSCRIPTION_KEY' = YOUR SUBSCRIPTION KEY

  Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
  This endpoint will be used in all examples in this quickstart.
 'FACE_ENDPOINT' = YOUR ENDPOINT

 

### To run the program :
 run main.py via python main.py or use IDE to run it .

### To excute request:
POST request to uri: http://localhost:5000/ with payload example describe below

   Input example:
   {
     "images":["http://google.com/photos/john-f-kennedy.jpg",
               "/images/image_1_kennedy.jpg"....]
   }

   Output example:
   {
       "code": 200,
       "message": "OK",
       "result": {
           "Image": "./images/image_1_kennedy.jpg",
           "Coordinates": {
               "Left(X)": 174,
               "Top(Y)": 285,
               "X+Width": 694,
               "Y+Height": 805
           }
       }
   }
