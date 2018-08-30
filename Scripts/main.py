import time

import Grid
import Intelligence
import Tile
import cv2
import numpy as np
from PIL import ImageGrab

# 6 is broken :)
screenshot_num = 0

if screenshot_num == 0:
    for count in range(3, 0, -1):
        print(count)
        time.sleep(1)
    full_img_bgr = np.array(ImageGrab.grab())
    full_img_rgb = cv2.cvtColor(full_img_bgr, cv2.COLOR_BGR2RGB)
    cv2.imwrite("../Images/Screenshots/ImageGrab.jpg", full_img_rgb)
    img_rgb = full_img_rgb[180:180 + 890, 580:580 + 690]

else:
    # Load image, select region, convert to grayscale.
    full_img_rgb = cv2.imread(f"..\Images\Screenshots\Screenshot {screenshot_num}.jpg")
    img_rgb = full_img_rgb[180:180 + 890, 580:580 + 690]

img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

grid = Grid.Grid()

# BGR
colours = {'red': (0, 0, 255), 'green': (0, 255, 0), 'orange': (0, 172, 255), 'pink': (172, 0, 255),
           'violet': (255, 0, 172)}
for col in colours:
    for pip in [True, False]:
        if pip:
            template = cv2.imread(f"../Images/Templates/{col}-pip.jpg", 0)
        else:
            template = cv2.imread(f"../Images/Templates/{col}.jpg", 0)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.92
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            # Over-matching fix: Only add/draw tiles that are far enough away from already found tiles.
            for t in grid.pre_tiles:
                dx = abs(pt[0] - t.ix)
                dy = abs(pt[1] - t.iy)
                if dx < 10 and dy < 10:
                    break
            else:  # I'm so happy that I used this! :)
                grid.pre_tiles.append(Tile.Tile(_ix=pt[0], _iy=pt[1], _colour=col, _pip=pip))

grid.setup_tiles()
print(grid)
AI = Intelligence.Intelligence(grid)
for t in grid.tiles:
    if t:
        t.text = str(t.index) + "|" + str(t.chained)
grid.draw(img_rgb)
print("...")
cv2.imshow('Result', img_rgb)
cv2.waitKey()
cv2.destroyAllWindows()

print("Done")

# DROP = -1
# PICK = 0
# SWITCH = 1
# LEFT = 2
# RIGHT = 3
# moves = [[PICK], [SWITCH, PICK], [PICK, SWITCH, DROP, SWITCH, PICK]]
