import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import json
import cv2


headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '15a1936620ae4de582888133557ae4cf',
}

params = urllib.parse.urlencode({
})


vidcap = cv2.VideoCapture(0)
# vidcap.set(cv2.CAP_PROP_FPS,5)
# fps = vidcap.get(cv2.CAP_PROP_FPS)
# print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
# success, image = vidcap.read()
count = 0
success = True


while success:
    success, image = vidcap.read()
    # print 'Read a new frame: ', success
    # frame = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    # processed_image = cv2.medianBlur(frame,5)

    cv2.imwrite("C:/Users/Roshan/Pictures/frame.jpg", image)  # save frame as JPEG file
    filename = 'C:/Users/Roshan/Pictures/frame.jpg'
    # count += 1
    # Replace the example URL below with the URL of the image you want to analyze.
    body = ""

    # load image
    f = open(filename, "rb")
    body = f.read()
    f.close()

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        faces = json.loads(data)
        for face in faces:
            a = face['scores']['anger']
            c = face['scores']['contempt']
            d = face['scores']['disgust']
            f = face['scores']['fear']
            h = face['scores']['happiness']
            s = face['scores']['sadness']
            p = face['scores']['surprise']
            print("Anger: ", a)
            print("Contempt: ", c)
            print("Disgust: ", d)
            print("Fear: ", f)
            print("Happiness: ", h)
            print("Sadness: ", s)
            print("Surprise: ", p)
       # print ("Response:")
       # print (json.dumps(parsed, sort_keys=True, indent=2))

        conn.close()
    except Exception as e:
        print(e.args)
