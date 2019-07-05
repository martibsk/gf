import numpy as np
import cv2
import copy
import time

board = 255 * np.ones(shape=[500, 500, 3], dtype=np.uint8)

cv2.rectangle(board, (0,0), (10,10), [255,0,0], thickness = 10)

cv2.imshow('cv', board)
key = cv2.waitKey(0) & 0xFF
