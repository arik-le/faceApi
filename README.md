# faceApi
Face API project

1.Detect Faces in Images.
2.Find Similar Faces of all the images.
3.Return the image and coordinates to the most common and largest face.

To run the program :
 run main.py via python main.py or use IDE to run it .

To excute request:
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
