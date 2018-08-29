import cv2
import numpy as np
from matplotlib import pyplot as plt

class Tile:
    def __init__(self, _ix, _iy, _colour):
        self.ix = _ix
        self.iy = _iy
        self.colour = _colour
        self.row = None
        self.col = int(round(_ix/100))

tiles = []

screenshot_num = 2

full_img_rgb = cv2.imread('..\Images\Screenshots\Screenshot ' + str(screenshot_num) + ".jpg")

img_rgb = full_img_rgb[180:180+890, 580:580+690]
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

#BGR
colours = {'red': (0,0,255), 'green': (0,255,0), 'orange':(0,172,255), 'pink': (172,0,255), 'purple': (255,0,172)}
for col in colours:
    template = cv2.imread(f"../Images/Templates/{col}.jpg",0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.92
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        # Over-matching fix: Only add/draw tiles that are far enough away from already found tiles.
        for t in tiles:
            dx = abs(pt[0]-t.ix)
            dy = abs(pt[1]-t.iy)
            if dx < 10 and dy < 10:
                break
        else: # I'm so happy that I used this! :)
            tiles.append(Tile(_ix=pt[0],_iy=pt[1],_colour=col))
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), colours[col], -1)
            # cv2.circle(img_rgb, (pt[0],pt[1]), 10, (255, 255, 255))

print(sorted([t.col for t in tiles]))

cv2.imshow('res.png',img_rgb)
cv2.waitKey()
cv2.destroyAllWindows()

print("done")