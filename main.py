import cv2
import pygame
from Morph import Morph
import time

# 480 x 640

# while True:
#
# # Делаем снимок
#     ret, frame = cam.read()
#
#     # Записываем в файл
#     cv2.imshow("cameraFeed", frame)
#     ch = cv2.waitKey(5)
#     if ch == 27:
#         break
#
# # Отключаем камеру
# cam.release()
# cv2.destroyAllWindows()

# exit()

pygame.init()
screen = pygame.display.set_mode((640, 480))
morph = Morph()
morph.positive_value = 1
morph.negative_value = 0
morph.set_SE([[1] * 3] * 3, 1, 1)
pivot = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    start = time.time()
    cam = cv2.VideoCapture(0)
    ret1, frame1 = cam.read()
    time.sleep(0.01)
    ret2, frame2 = cam.read()
    cam.release()
    print('two picture were made in', time.time() - start, 'seconds')

    start = time.time()
    width = len(frame1[0])

    frame1 = frame1.tolist()
    frame2 = frame2.tolist()
    result_image = []

    # bring the image to a monochrome appearance
    for i in range(len(frame1)):
        result_image.append([])
        for j in range(width):
            value = abs((0.2125 * frame1[i][j][0]) + (0.7154 * frame1[i][j][1]) + (0.0721 * frame1[i][j][2]) - (0.2125 * frame2[i][j][0]) - (0.7154 * frame2[i][j][1]) - (0.0721 * frame2[i][j][2]))
            result_image[i].append(0 if value < pivot else 1)

    print('monochrome picture was made in', time.time() - start, 'seconds')
    start = time.time()

    morph.set_binary_image(result_image)
    morph.opening(keep_sizes=True)
    result_image = morph.binary_image
    print('picture was processed with MP in', time.time() - start, 'seconds')
    start = time.time()

    for i in range(480):
        for j in range(640):
            color = (0, 0, 0) if result_image[i][j] == 0 else (255, 255, 255)
            screen.set_at((j, i), color)


    pygame.display.update()
    print('picture was displayed in', time.time() - start, 'seconds', end='\n' + '-' * 10 + '\n')

# cam.release()

cv2.destroyAllWindows()
