import numpy as np
import pyautogui
import time


distFactor = 95

rows, cols = (8, 8)
initial_point = np.array([302.5, 887.5])

coordMatrix = np.zeros((rows, cols, 2))

for row in range(rows):
    for col in range(cols):
        coordMatrix[row, col] = initial_point + np.array([distFactor * col, -distFactor * row])
        

print("Calibrating in 3 seconds...")
time.sleep(3)

#Move the mouse to each position in the coordMatrix
for row in range(rows):
    for col in range(cols):
        pyautogui.moveTo(coordMatrix[row][col][0], coordMatrix[row][col][1])
        time.sleep(0.5)