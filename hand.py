import cv2
import numpy as np
from matplotlib import pyplot as plt


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# camera id, screen size
def video_capture(camera, width, height):
    capture = cv2.VideoCapture(camera)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    success, f = capture.read()
    if success:
        return f


# threshold the each pixel to separate skin color and get a binary image
def threshold(R, G, B):
    if ((R > 95) and (G > 40) and (B > 20) and ((max(R, max(G, B)) - min(R, min(G, B))) > 15) and
            (abs(R - G) > 15) and (R > G) and (R > B)) or ((R > 220) and (G > 120) and (B > 170) and
                                                               (abs(R > G) <= 15) and (G > B)):
        return True


def face_detection(image):
    face = face_cascade.detectMultiScale(image, 1.1, 5)
    for(x, y, w, h) in face:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1)
        face_detected = image[y:y+h, x:x+w]
        image[y+h, x+w] = [0, 0, 0]
    return image


while cv2.waitKey(27) < 0:
    # success, frame = video.read()
    # count = 0
    frame = video_capture(0, 1280, 720)
    # print var = 'Read a new frame: ', success
    # cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
    # cv2.putText(frame, "Frame No: %d" % count, (50, 50), cv2.FONT_ITALIC, 0.5, 125)
    res = cv2.resize(frame, (256, 144), interpolation=cv2.INTER_LINEAR)
    # cv2.imshow('Video1', res)
    # plt.hist(res.ravel(), 256, [0, 256])
    plt.show()
    for pix in range(1, 144):
        for piy in range(1, 256):
            b = res[pix, piy, 0]
            g = res[pix, piy, 1]
            r = res[pix, piy, 2]
            if threshold(r, g, b):
                res[pix, piy] = 255  # make white
            else:
                res[pix, piy] = 0  # make black

    filtered_image = cv2.medianBlur(res, 3)
    face = face_detection(filtered_image)
    cv2.imshow('Video', face)
    # cv2.imshow('Filtered',filtered_image)
    # count += 1
    # img = cv2.resize(frame, (160, 90))
    # cv2.imwrite("resize.jpg", img)
