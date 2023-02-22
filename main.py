import cv2
from Morph import Morph
import time


morph = Morph()
morph.positive_value = 1
morph.negative_value = 0
morph.set_SE([[1] * 3] * 3, 1, 1)

pivot = 10

while True:
    # make two frames
    cam = cv2.VideoCapture(0)
    ret1, frame1 = cam.read()
    time.sleep(0.01)
    ret2, frame2 = cam.read()
    cam.release()

    width = len(frame1[0])

    frame1 = frame1.tolist()
    frame2 = frame2.tolist()
    result_image = []

    # bring the image to a monochrome appearance and subtract one from other
    for i in range(len(frame1)):
        result_image.append([])
        for j in range(width):
            value = abs((0.2125 * frame1[i][j][0]) + (0.7154 * frame1[i][j][1]) + (0.0721 * frame1[i][j][2]) - (0.2125 * frame2[i][j][0]) - (0.7154 * frame2[i][j][1]) - (0.0721 * frame2[i][j][2]))
            result_image[i].append(0 if value < pivot else 1)

    # apply morphological processing
    morph.set_binary_image(result_image)
    morph.opening(keep_sizes=True)
    result_image = morph.binary_image

    # find square of result_image
    square = 0
    for i in range(len(result_image)):
        for j in range(width):
            if result_image[i][j] == 1:
                square += 1

    print(square)

cv2.destroyAllWindows()
